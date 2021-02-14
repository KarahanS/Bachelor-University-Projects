#include <iostream>
#include <vector>
#include <queue>

#ifndef GRAPH_H
#define GRAPH_H

using namespace std;

class Graph {
private:
	vector<vector<int>> adjacencyList;
	vector<int> inDegree;
	int noV;
	int noE;
public:
	Graph(int V);
	void add(int v, int w, int ind);
	int V();
	int E();
	vector<int>& adj(int v);
	void removeEdge(int v);
	bool isEulerian(int v);

};

#endif // GRAPH_H