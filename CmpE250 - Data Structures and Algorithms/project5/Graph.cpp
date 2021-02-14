#include "Graph.h"

Graph::Graph(int V) {
	this->noV = V;
	this->noE = 0;
	c = 0;

	labels = new depth_label[V]; 
	hashTable.push_back(-1);

	// cout << "Graph is constructed." << endl;
	for(int i=0; i<V; i++) {
		adjacencyList.push_back(vector<int> ());
	}
}


void Graph::add(int v, int w) {
	// Directed Graph
	adjacencyList[v].push_back(w);
	this->noE++;

}
// depth starts from 0
void Graph::DFS(int node, int depth) {
	c++;
	labels[node] = depth_label(depth, c);
	hashTable.push_back(node);
	// cout << "We are at " << node << " " << " depth : " << depth << "  label :" << c << endl;

	while(dynamicArray.size() <= depth) {
		dynamicArray.push_back(vector<int> ());
	}

	dynamicArray[depth].push_back(c);
	for(int w: adjacencyList[node]) {
		DFS(w, depth+1);
	}
}

int Graph::V() {
	return this->noV;
}
int Graph::E() {
	return this->noE;
}

vector<int>& Graph::adj(int v) {
	return this->adjacencyList[v];
}

depth_label& Graph::depth_n_label(int node){
	return labels[node];
}
vector<int>& Graph::array(int depth) {
	// cout << depth << " " << dynamicArray.size() << endl;
	return this->dynamicArray[depth];
}
int Graph::hash(int label) {
	return hashTable[label];
}
Graph::~Graph() {
	delete[] this->labels;
}

