#include <iostream>
#include <fstream>
#include <string>
#include "Graph.h"

using namespace std;

int findAncestor(int depth, int l, int lo, int hi, Graph& graph);

int main(int argc, char const *argv[])
{

	string infile_name = argv[1];
	string outfile_name = argv[2];

	ifstream infile;
	ofstream outfile;

	infile.open(infile_name);
	outfile.open(outfile_name);

	int V;
	infile >> V;
	// cout << "V --> " << V  << endl;

	Graph graph(V);

	// edge (v, w) means, v is parent of w
	int v;
	infile >> v; 
	for(int w=1; w<graph.V(); w++) {
		infile >> v;
		graph.add(v, w);    // v is parent of w
	}
	graph.DFS(0, 0);
	// cout << " Starting " << endl;

	int T;
	infile >> T;
	for(int i=0; i<T; i++) {
		// queries
		int node, n;

		// depth of node = x
		// depth of ancestor = y

		// depth of ancestor = depth of node - n;

		infile >> node >> n;
		int label = graph.depth_n_label(node).second;
		int d = graph.depth_n_label(node).first;

		int depth = d - n;
		// ancestor of node at depth n

		// cout << "Depth of the ancestor --> " << d << endl;
		// cout << "on query = " << node << " || label = " << label << endl;

		int lo = 0;
		// cout << " Error ? " << endl;
		if(depth >= 0) {
			int hi = graph.array(depth).size() - 1;
			int labelOfAncestor = findAncestor(depth, label, lo, hi, graph);
			outfile << graph.hash(labelOfAncestor) << endl;
		} else {
			outfile << -1 << endl;
		}

		
	}

	infile.close();
	outfile.close();

	// cout << "End of the session" << endl;
	return 0;
}

// look up the largest element s, smaller than l ( s and l are labels in dynamic array)
int findAncestor(int depth, int label, int lo, int hi, Graph& graph) {
	int mid = lo + (hi-lo)/2;
	// cout << " There is a problem here" << endl;

	if( graph.array(depth)[mid] > label) {
		return findAncestor(depth, label, lo, mid-1, graph);     
	} else if ( graph.array(depth)[mid] < label) {
		if(mid == graph.array(depth).size() -1) return graph.array(depth)[mid];
		else {
			if( graph.array(depth)[mid+1] > label) return graph.array(depth)[mid];
			else return findAncestor(depth, label, mid+1, hi, graph);
		}
	} else { /* impossible */ }

	return 0;

}