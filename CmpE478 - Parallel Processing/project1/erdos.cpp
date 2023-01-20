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

#include <chrono> // timer
using namespace std;

unordered_map<string, int> hashmap;  // domain --> index
unordered_map<int, string> indices;  // index --> domain 
unordered_map<int, vector<int>> adj; // adjacency list for the graph
unordered_map<int, int> outdegree;
int idx = 0;
int nIterations = 0;

// CSR data structures
vector<int> row_begin;
vector<double> values;
vector<int> col_indices;

// Constants
double alpha = 0.2;
double epsilon = 1e-6;

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
        if(outdegree.find(f) == outdegree.end()) outdegree[f] = 1;  // keep a vector of outdegrees
        else outdegree[f]++;
    }

    stream.close();

    row_begin.push_back(0);
    for (int i = 0; i < adj.size(); i++)
    {
        row_begin.push_back(row_begin.back() + adj[i].size());
        for (int j = 0; j < adj[i].size(); j++)
            col_indices.push_back(adj[i][j]);
    }

    int N = row_begin.size() - 1;
    for (int i = 0; i < N; i++)
    {
        for(int j = row_begin[i]; j < row_begin[i + 1]; j++) 
        {
            int from = col_indices[j];      // website T_i which has a citation to our website A
            double outd = outdegree[from];  // calculate C_i of the website (outdegree) 
            values.push_back(1/outd);    
        }
    }
}

// Calculates the rank of the pages - returns a vector with N elements 
vector<double> calc()
{
    nIterations = 0;
    int N = row_begin.size() - 1;
    vector<double> r1(N, 1.0);
    vector<double> r2(N, 1.0);

    while (true)
    {
        double cSum = 0;
        // parallelize the matrix multiplication
        #pragma omp parallel for default(shared) schedule(runtime) reduction(+: cSum)
        for (int i = 0; i < N; i++)
        {        
            double sum = 0;
            #pragma omp parallel for default(shared) schedule(runtime) reduction(+: sum)
            for(int j = row_begin[i]; j < row_begin[i + 1]; j++) 
            {
                int from = col_indices[j];  // website T_i which has a citation to our website A
                sum += r1[from]*values[j];  // r1 * (1/C_i)
            }
            r2[i] = alpha * sum  + (1 - alpha);
            cSum += abs(r1[i] - r2[i]);
        }
        nIterations++;               // increment number of iterations
        if (cSum <= epsilon) break;  // break if the sum is less than epsilon
        r1 = r2;
    }

    return r1;
}

// Returns the names of the first 5 hosts that have the highest rankings.
vector<string> getFive(vector<double>& r1) {
    vector<pair<double, int>> pairs;
    for(int i=0; i<r1.size(); i++) 
        pairs.push_back(pair<double, int>(r1[i], i));

    // sort the (host, page rank) pairs
    sort(pairs.begin(), pairs.end());
    vector<string> firstFive;
    for(int i=1; i <= 5; i++) {        
        int idx = pairs[pairs.size() - i].second;
        firstFive.push_back(indices[idx]);
    }
    return firstFive;
    
}

int main()
{
    cout << "Input is read sequentially - it'll take a while." << endl;
    auto start = chrono::high_resolution_clock::now();
    toCSR("graph.txt");

    std::ofstream myfile;
    // create the csv file
    myfile.open ("timings.csv");
    myfile << "Test No.,Scheduling Method,Chunk Size,No. of Iterations, Timings, in, secs, for, each, number, of, threads\n";
    myfile << ",,,,1,2,3,4,5,6,7,8\n";

    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::seconds>(stop - start);
    cout << "Total amount of time to read the file: " << duration.count() << " seconds" << endl;

    string types[3] = {"omp_sched_static", "omp_sched_dynamic", "omp_sched_guided"};

    for(int ii= 0; ii<3; ii++){
        if(ii==0){
            // Tell OpenMP which scheduling kind and chunk size use for runtime schedule clauses
	        omp_set_schedule(omp_sched_static, 20000);
        }
        else if(ii==1){
            // Tell OpenMP which scheduling kind and chunk size use for runtime schedule clauses
	        omp_set_schedule(omp_sched_dynamic, 20000);
        }
        else{
            // Tell OpenMP which scheduling kind and chunk size use for runtime schedule clauses
	        omp_set_schedule(omp_sched_guided, 20000);
        }

        myfile << ii << "," << types[ii] << "," << "2" << ",";

        for(int jj=1; jj<9; jj++){
            // Use jj many threads when creating OpenMP parallel regions
	        omp_set_num_threads(jj);

            start = chrono::high_resolution_clock::now();
            vector<double> r1 = calc();
            stop = chrono::high_resolution_clock::now();
            duration = chrono::duration_cast<chrono::seconds>(stop - start);
            cout << "Total amount of time spent for rank calculation: " << duration.count() << " seconds. #threads: " << omp_get_max_threads() << ", schedule type: " << types[ii] << endl;
            
            if(jj==1) myfile << nIterations << ",";
            myfile << duration.count();
            if(jj<8){
                myfile<< ",";
            }
        }
        myfile << "\n";
        cout<< "\n";
    }
    
    vector<double> r1 = calc();
    vector<string> firstFive = getFive(r1);
    cout << "Names of the first 5 hosts that have the highest rankings (from first to fifth):" << endl;
    for(auto& c: firstFive) cout << c << " ";

    myfile.close();
    return 0;
}
