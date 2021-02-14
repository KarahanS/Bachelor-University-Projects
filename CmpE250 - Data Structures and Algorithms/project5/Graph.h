#include <iostream>
#include <vector>
#include <queue>

#ifndef GRAPH_H
#define GRAPH_H

using namespace std;

typedef pair<int, int> depth_label;

class Graph {
private:
	vector<vector<int>> adjacencyList;
	vector<vector<int>> dynamicArray;
	depth_label* labels;
	vector<int> hashTable;
	int noV;
	int noE;
	int c = 0;
public:
	Graph(int V);
	void add(int v, int w);
	void DFS(int node, int level);
	int V();
	int E();
	vector<int>& adj(int v);
	depth_label& depth_n_label(int node);
	vector<int>& array(int depth);
	int hash(int label);
	~Graph();

};

#endif // GRAPH_H