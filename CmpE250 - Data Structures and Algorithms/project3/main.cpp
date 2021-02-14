#include <iostream>
#include <string>
#include <fstream>
#include "Graph.h"

using namespace std;

int main(int argc, char const *argv[]) {

	// 1) starting index is already given
	// 2) When there are more than one traverse options, traverse the edge that 
	// is connected to the vertex with the lowest ID
	// 3) To start a new tour, use the vertex that is closes to the beginning of
	// the current circuit.




	string infile_name = argv[1];
	string outfile_name = argv[2];

	ifstream infile;
	ofstream outfile;

	infile.open(infile_name);

	int V;
	infile >> V;

	Graph G = Graph(V);


	for(int i=0; i<G.V(); i++) {
		int v, noAdjacents;
		infile >> v >> noAdjacents;

		G.adj(v).resize(noAdjacents);
		for(int adj = 1; adj <= noAdjacents; adj++) {
			int w;
			infile >> w;
			G.add(v, w, noAdjacents - adj);
		
		}



		// sort(G.adj(v).begin(), G.adj(v).end()); --> edges will always be given in sorted order (resource = QA on Project 3)
	}


	int v;
	infile >> v;



	bool isEulerian = true;
	for(int vertex=0; vertex<G.V(); vertex++) {
		if(!G.isEulerian(vertex)) {
			isEulerian = false;
			break;
		}
	}

	outfile.open(outfile_name);

	if(isEulerian) {

		vector<int> circuit;
		circuit.push_back(v);

		while(circuit.size() <= G.E()) {

		    // cout << "Circuit is being constructed." << endl;
			vector<int> tour;
			int start = v;

			// since we sorted array, it always starts to check from the lowest ID



			while(!G.adj(v).empty()) {
			    // cout << " Looking for an edge to traverse " << endl;
			    int to = G.adj(v).back();
			    G.removeEdge(v);   // to is removed from the graph
			    v = to;
			    tour.push_back(v);
			} 



			// merge
			// cout << "Merge" << endl;
			int ind = 0;
			while(circuit[ind] != start) ind++;
			auto it = circuit.begin() + ind + 1;  // start is in circuit.begin() + ind, we should start from circuit.begin() + ind + 1.
			circuit.insert(it, tour.begin(), tour.end());

			// find a vertex in the circuit with non-traversed outgoing edges

			for(int k: circuit) {
				if(!G.adj(k).empty()) {
					v = k;
					break;
				}
			}
		}

		for(int i=0; i<circuit.size(); i++) outfile << circuit[i] << " ";
	} else {

		outfile << "no path";

	}

	infile.close();
	outfile.close();


	return 0;
}