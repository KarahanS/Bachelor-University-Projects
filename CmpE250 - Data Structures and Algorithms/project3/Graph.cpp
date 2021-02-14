#include "Graph.h"

Graph::Graph(int V) {
	this->noV = V;
	this->noE = 0;


	for(int i=0; i<V; i++) {
		vector<int> v;
		adjacencyList.push_back(v);
		inDegree.push_back(0);
	}
}

bool Graph::isEulerian(int v) {
	return adjacencyList[v].size() == inDegree[v];
}
void Graph::removeEdge(int v) {
	adjacencyList[v].pop_back();
}

void Graph::add(int v, int w, int ind) {
	// Directed Graph
	adjacencyList[v][ind] = w;
	this->noE++;
	inDegree[w]++;
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


