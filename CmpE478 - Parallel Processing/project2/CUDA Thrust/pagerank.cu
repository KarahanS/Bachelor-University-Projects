#include <stdio.h>
#include <omp.h>
#include <unordered_map>
#include <cmath> // for abs

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string.h>
#include <algorithm>    // std::sort

// thrust
#include <thrust/host_vector.h>	
#include <thrust/device_vector.h>	
#include <thrust/generate.h>	
#include <thrust/sort.h>	
#include <thrust/copy.h>		
#include <thrust/inner_product.h>	
#include <thrust/gather.h>


#include <chrono> // timer
using namespace std;

unordered_map<string, int> hashmap;  // domain --> index
unordered_map<int, string> indices;  // index --> domain 
unordered_map<int, vector<int>> adj; // adjacency list for the graph
unordered_map<int, int> outdegree;
int idx = 0;
int nIterations = 0;
int occupiedRows = 0;

// CSR data structures
vector<int> row_begin;
vector<float> values;
vector<int> col_indices;
vector<int> rows;
vector<int> nonOccupiedRows;
// Constants
float alpha = 0.2;
float epsilon = 1e-3;  // not 1e-6 because of float precision

struct func
{
  __device__ float operator()(thrust::tuple<float, float> t) 
  {
     float f = thrust::get<0>(t) - thrust::get<1>(t);
     return abs(f);
  }
};


struct multiply_add
{
  __host__ __device__
  float operator()(float x) const
  {
    // define alpha as a constant
    const float alpha = 0.2f;

    // multiply x by alpha and add alpha - 1
    return x * alpha + (1.0f - alpha);
  }
};

// Reads the file and converts it to CSR format.
void toCSR(string file)
{
    ifstream stream(file);
    string line;

    while (getline(stream, line))
    {
        string from, to;
        stringstream ss(line);
        ss >> from;
        ss >> to;

        int f, t = 0;
        if (hashmap.find(from) == hashmap.end()){
            hashmap[from] = idx;
            indices[idx] = from;
            f = idx++;
        } else f = hashmap[from];
        if (hashmap.find(to) == hashmap.end()) {
            hashmap[to] = idx;
            indices[idx] = to;
            t = idx++;
        } else t = hashmap[to];

        if (adj.find(f) == adj.end()) adj[f] = {};
        if (adj.find(t) == adj.end()) adj[t] = {};

        adj[t].push_back(f); // we want Q_ij to be marked if there is a link from j(th) page to i(th) page.
        if(outdegree.find(f) == outdegree.end()) outdegree[f] = 1;
        else outdegree[f]++;
    }

    stream.close();

    row_begin.push_back(0);
    for (int i = 0; i < adj.size(); i++)
    {
        bool occupied = false;
        row_begin.push_back(row_begin.back() + adj[i].size());
        for (int j = 0; j < adj[i].size(); j++) {
            col_indices.push_back(adj[i][j]);
            rows.push_back(i);
            occupied = true;
        }
        if (occupied) occupiedRows++;
        else nonOccupiedRows.push_back(i);
    }

    int N = row_begin.size() - 1;
    for (int i = 0; i < N; i++)
    {
        for(int j = row_begin[i]; j < row_begin[i + 1]; j++) 
        {
            int from = col_indices[j];   // website T_i which has a citation to our website A
            float outd = outdegree[from];  // calculate C_i of the website (outdegree)
            values.push_back(1/outd);      // find in unordered_map could take worst case O(n), linked list structure faster or array 
        }
    }
}


// Returns the names of the first 5 hosts that have the highest rankings.
vector<string> getFive(thrust::device_vector<float>& r1) {
    thrust::device_vector<int> index(r1.size());
    thrust::sequence(index.begin(), index.end()); // 0, 1, 2, 3, ...
    thrust::sort_by_key(r1.begin(), r1.end(), index.begin());

    vector<string> firstFive;
    for(int i= index.size() - 1; i >= index.size() - 5; i--) {  
        int idx = index[i];   
        firstFive.push_back(indices[idx]);
    }
    return firstFive;
    
}

int main()
{   
    
    cout << "Input is read sequentially - it'll take a while." << endl;
    auto start = chrono::high_resolution_clock::now();
    toCSR("../graph.txt");
    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::seconds>(stop - start);
    cout << "Total amount of time to read the file: " << duration.count() << " seconds" << endl;
    auto io = duration.count();

    std::ofstream myfile;
    myfile.open ("timings.csv");
    myfile << "I/O - CSR transformation, Pagerank Algorithm\n";

    
    start = chrono::high_resolution_clock::now();
    int N = row_begin.size() - 1;
    // thrust CSR
    nIterations = 0;
    thrust::device_vector<float> r1(N, 1.0);
    thrust::device_vector<float> col_indices_d(col_indices.begin(), col_indices.end());
    thrust::device_vector<float> values_d(values.begin(), values.end());
    thrust::device_vector<int> rows_d(rows.begin(), rows.end());
    thrust::device_vector<int> nonOccupied(nonOccupiedRows.begin(), nonOccupiedRows.end());
    while (true)
    {
        thrust::device_vector<float> r2(N, 0.0);
        thrust::device_vector<int> ind(occupiedRows, 0);
        thrust::device_vector<float> P(col_indices_d.size(), 0);

        // cout << col_indices.size() << endl;
        thrust::transform(
            thrust::make_permutation_iterator(r1.begin(), col_indices_d.begin()),
            thrust::make_permutation_iterator(r1.end(), col_indices_d.end()),
            values_d.begin(), P.begin(), thrust::multiplies<float>());

        thrust::reduce_by_key(
            rows_d.begin(), rows_d.end(),
            P.begin(), ind.begin(), r2.begin());
        // https://github.com/NVIDIA/thrust/issues/1621 ?
        thrust::device_vector<int> indextended = ind;
        indextended.reserve(nonOccupied.size());
        indextended.insert(indextended.end(), nonOccupied.begin(), nonOccupied.end());
        thrust::sort_by_key(indextended.begin(), indextended.end(), r2.begin());
        
        thrust::transform(r2.begin(), r2.end(), r2.begin(), multiply_add());
        float cSum = thrust::transform_reduce(
            thrust::make_zip_iterator(thrust::make_tuple(r1.begin(), r2.begin())), 
            thrust::make_zip_iterator(thrust::make_tuple(r1.end(), r2.end())), 
            func(), 0.0f, thrust::plus<float>());

        nIterations++;
        if (cSum <= epsilon) break;
        thrust::copy(r2.begin(), r2.end(), r1.begin());  // copy r2 to r1: r1 = r2
    }

    stop = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::seconds>(stop - start);
    myfile << io << "," << duration.count() << "\n";
    cout << "Total amount of time to calculate the pagerank: " << duration.count() << " seconds" << endl;

    vector<string> firstFive = getFive(r1);
    cout << "Names of the first 5 hosts that have the highest rankings (from first to fifth):" << endl;
    for(auto& c: firstFive) cout << c << "\n";
    
    myfile.close();
    return 0;
}

/**
 * 4mekp13kca78a3hfsrb0k813n9 0491md82hej8u15vi98isrmuih 3165mii1s1g0invqs94q303v0v 46o3c5beh6kiojkvr1tvsk4ptt 2494c7mt12frm3c3go86abe13h
*/