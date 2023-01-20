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

#include <mpi.h> // ms mpi
using namespace std;

unordered_map<string, int> hashmap;  // domain --> index
unordered_map<int, string> indices;  // index --> domain 
unordered_map<int, int> nodeToProcessor;  // index --> processorID 
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


        //transpose the graph by reversing from and to 
        string temp = from;
        from = to;
        to = temp;

        int f, t = 0;
        if (hashmap.find(from) == hashmap.end()) {
            hashmap[from] = idx;
            indices[idx] = from;
            f = idx++;
        }
        else f = hashmap[from];
        if (hashmap.find(to) == hashmap.end()) {
            hashmap[to] = idx;
            indices[idx] = to;
            t = idx++;
        }
        else t = hashmap[to];

        //values.push_back(1); //? to keep count?
        if (adj.find(f) == adj.end()) adj[f] = {};
        if (adj.find(t) == adj.end()) adj[t] = {};


        adj[t].push_back(f); // we want Q_ij to be marked if there is a link from j(th) page to i(th) page.
        if (outdegree.find(t) == outdegree.end()) outdegree[t] = 1;
        else outdegree[t]++;
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
        for (int j = row_begin[i]; j < row_begin[i + 1]; j++)
        {
            double outd = outdegree[i];  // calculate C_i of the website (outdegree)
            values.push_back(1 / outd);                          //find in unordered_map could take worst case O(n), linked list structure faster or array ?
        }
    }
}


// Returns the names of the first 5 hosts that have the highest rankings.
vector<string> getFive(vector<double>& r1) {
    vector<pair<double, int>> pairs;
    for (int i = 0; i < r1.size(); i++) {
        pairs.push_back(pair<double, int>(r1[i], i));
    }


    sort(pairs.begin(), pairs.end());
    vector<string> firstFive;
    for (int i = 1; i <= 5; i++) {
        int idx = pairs[pairs.size() - i].second;
        firstFive.push_back(indices[idx]);
    }
    return firstFive;

}

int main(int argc, char** argv)
{
    int mypid;
    int numprocs;

    //temporary storage for broadcasting
    vector <string> hashes;
    vector <int> indexes;
    vector <int> nodeFrom;
    vector <int> nodeTo;

    int l = 0;
    int n = 0;
    int r = 0;
    int v = 0;
    int c = 0;

    //keeps the beginning addresses(indexes) of all the nodes assigned to my processor
    vector <int> row_of_processor;
    vector <int> my_indexes;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &mypid);        /* get current process id */
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);     /* get number of processes */


    
    auto start = chrono::high_resolution_clock::now();

    if (mypid == 0) {

        cout << "Input is read sequentially - it'll take a while." << endl;
        ifstream stream("partitions/p" + std::to_string(numprocs) + ".txt");
        if(!stream.good()) {
            cout << "There is no corresponding partition file with the given number of processors. Please first use partition.py to generate required partitions." << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
            return 0;
        }
        toCSR("../graph.txt");

        string line;

        while (getline(stream, line))
        {
            string from, to;
            stringstream ss(line);
            ss >> from;
            ss >> to;

            int nodeIndex = hashmap[from];
            if (nodeToProcessor.find(nodeIndex) == nodeToProcessor.end()) {
                nodeToProcessor[nodeIndex] = stoi(to);
            }
        }
        stream.close();

        l = hashmap.size();

        n = nodeToProcessor.size();
        r = row_begin.size();
        c = col_indices.size();
        v = values.size();

        for (const auto& n : hashmap) {
            hashes.push_back(n.first);
            indexes.push_back(n.second);
        }

        for (const auto& n : nodeToProcessor) {
            nodeFrom.push_back(n.first);
            nodeTo.push_back(n.second);
        }
    }
    MPI_Bcast(&l, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&r, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&v, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&c, 1, MPI_INT, 0, MPI_COMM_WORLD);


    if (mypid != 0) {

        for (int i = 0; i < l; i++ ) {
            hashes.push_back("4a073uf3rv3m6mrk57sh7v6vib");
            indexes.push_back(i);
        }

        for (int i = 0; i < n; i++) {
            nodeFrom.push_back(i);
            nodeTo.push_back(n-i);
        }

        for (int i = 0; i < r; i++) {
            row_begin.push_back(i);
        }

        for (int i = 0; i < v; i++) {
            values.push_back(i);
        }

        for (int i = 0; i < c; i++) {
            col_indices.push_back(i);
        }
    }


        //MPI_Bcast
        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Bcast(&row_begin.front(), row_begin.size(), MPI_INT, 0, MPI_COMM_WORLD);
        //MPI_Barrier(MPI_COMM_WORLD);
        MPI_Bcast(&values.front(), values.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);
        //MPI_Barrier(MPI_COMM_WORLD);
        MPI_Bcast(&col_indices.front(), col_indices.size(), MPI_INT, 0, MPI_COMM_WORLD);


        ///* Broadcast each line */
        for (int i = 0; i < l; i++)
            MPI_Bcast(&hashes[i], 27, MPI_CHAR, 0, MPI_COMM_WORLD);
            
        MPI_Bcast(&indexes.front(), l, MPI_INT , 0, MPI_COMM_WORLD);

        MPI_Bcast(&nodeFrom.front(), nodeFrom.size(), MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&nodeTo.front(), nodeTo.size(), MPI_INT, 0, MPI_COMM_WORLD);

        MPI_Barrier(MPI_COMM_WORLD);
        if (mypid != 0) {
            for (int i = 0; hashes.size() < l; i++) {
                hashmap[hashes[i]] = indexes[i];
            }

            for (int i = 0; i < nodeFrom.size(); i++) {
                nodeToProcessor[nodeFrom[i]] = nodeTo[i];
            }
        }


    //toCSR("graph.txt");

    std::ofstream myfile;
    myfile.open("timingsMPI.csv");
    //myfile << "Test No.,Scheduling Method,Chunk Size,No. of Iterations, Timings, in, secs, for, each, number, of, threads\n";
    //myfile << ",,,,1,2,3,4,5,6,7,8\n";

    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::seconds>(stop - start);

    auto io = duration.count();

    if (mypid == 0) {
        cout << "Total amount of time to read the file: " << duration.count() << " seconds" << endl;
    }


    int N = row_begin.size() - 1;

    vector<double> r0(N, 1.0);
    vector<double> r1(N, 1.0);



    //just as a temp so that we can keep pushing and popping next end
    row_of_processor.push_back(0);

    //get which nodes are appointed to this processor ??????? +1
    for (int i = 0; i < N; i++) {
        //if node is appointed to this processor
        if (nodeToProcessor[i] == mypid) {
            row_of_processor.pop_back();
            row_of_processor.push_back(row_begin[i]);
            row_of_processor.push_back(row_begin[i + 1]);
            my_indexes.push_back(i);
        }
    }

    double cSum = 10 * epsilon;
    int numIter = 0;

    for (int i = 0; i < N; i++) {
        //initiaize array for each iteration
        r1[i] = 1.0;
    }

    start = chrono::high_resolution_clock::now();

    //check diff
    while (cSum > epsilon) {
        cSum = 0;
        numIter++;
        r0 = r1;

        //should be initialized only once to 1-alpha
        if (mypid == 0) {
            for (int i = 0; i < N; i++) {
                //initiaize array for each iteration
                r1[i] = (1 - alpha);
            }
        }
        else {
            for (int i = 0; i < N; i++) {
                //initiaize array to 0 for each iteration
                r1[i] = 0;
            }
        }

        //matrix multiplication r1 = my_ranks*(my part of P)
        for (int i = 0; i < my_indexes.size(); i++) {
            for (int j = row_begin[my_indexes[i]]; j < row_begin[my_indexes[i] + 1]; j++) {

                r1[col_indices[j]] += alpha * r0[my_indexes[i]] * values[j]; 
            }
        }

        //barrier- synchronize
        MPI_Barrier(MPI_COMM_WORLD);

        //reduceall 
            //STL vectors are guaranteed to have contiguously allocated memory. That is, you can treat them like C arrays by getting a pointer to the first element.
        MPI_Allreduce(MPI_IN_PLACE, &r1.front(), r1.size(), MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

        //calculate r0 and r1 diff in parallel
        double localDiff = 0.0;
        for (int index : my_indexes) {
            localDiff += abs(r0[index] - r1[index]);
        }
        cSum = 0.0;
        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Allreduce(&localDiff, &cSum, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

    }

    stop = chrono::high_resolution_clock::now();
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Allreduce(MPI_IN_PLACE, &stop, 1, MPI_LONG, MPI_MAX, MPI_COMM_WORLD);


    if (mypid == 0) {
        
        duration = chrono::duration_cast<chrono::seconds>(stop - start);
        myfile << io << "," << duration.count() << "\n";
        cout << "Total amount of time to calculate the pagerank: " << duration.count() << " seconds" << endl;
    }



    if (mypid == 0) {
        //vector<double> r1 = calc();
        vector<string> firstFive = getFive(r1);
        //cout << "Names of the first 5 hosts that have the highest rankings (from first to fifth):" << endl;
        for (auto& c : firstFive) cout << c << " " << endl;
        cout << "Number of iter: " << numIter << endl;

    }

    MPI_Finalize();

    myfile.close();
    return 0;
}
