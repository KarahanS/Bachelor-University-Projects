#include <iostream>
#include <string>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <stack>
#include <limits>
#include <queue>

using namespace std;

typedef pair<int, int> CostCapacity;

// inspired by <https://github.com/rizaozcelik/cmpe250-fall20/blob/main/PS11/ford_fulkerson.cpp>" 
struct AugmentingPath {
	int bottleneck;
	int cost;
	stack<int> path;

	AugmentingPath() {
		this->bottleneck = -1;
	}
	AugmentingPath(int bottleneck, int cost, stack<int> path) {
		this->bottleneck = bottleneck;
		this->cost = cost;
		this->path = path;
	}
};

// inspired by <https://github.com/rizaozcelik/cmpe250-fall20/blob/main/PS11/ford_fulkerson.cpp>" 
// finds an augmenting path using DFS
AugmentingPath findAugmentingPath(vector<unordered_map<int, CostCapacity>>& residualGraph, int source, int sink) {

	stack<int> path;
	stack<int> stack;
	stack.push(source);

	int parent[residualGraph.size()];     
	for(int i=0; i<residualGraph.size(); i++) {
		parent[i] = -1;
	}
	parent[source] = source;	

	while(!stack.empty() && parent[sink] == -1) {
		int v = stack.top();
		stack.pop();
		for(const auto& pair: residualGraph[v]) {
			int w = pair.first;   // to vertex
			if(parent[w] == -1) {
				parent[w] = v;
				stack.push(w);
			}
		}		
	}

	if(parent[sink] == -1) return AugmentingPath();
	int bottleneck = numeric_limits<int>::max();

	int vertex = sink;
	int cost = 0;
	while(vertex != source) {
		path.push(vertex);
		int from = parent[vertex];

		cost+= residualGraph[from][vertex].first;
		int flow = residualGraph[from][vertex].second;   // first = cost   second = capacity
		if(bottleneck > flow) bottleneck = flow;

		vertex = from;
	}

	path.push(source);
	AugmentingPath aug(bottleneck, cost, path);

	return aug;
}


void augment(vector<unordered_map<int, CostCapacity>>& residualGraph, AugmentingPath& augPath) {

	int bottleneck = augPath.bottleneck;
	stack<int> path = augPath.path;

	// first element in stack is the source
	while(path.size() > 1) {
		int from = path.top();
		path.pop();
		int to = path.top();
		int cost = residualGraph[from][to].first;

		int remainingCapacity = residualGraph[from][to].second - bottleneck;

		if(remainingCapacity == 0) residualGraph[from].erase(to);
		else  residualGraph[from][to].second = remainingCapacity;
		

		// now it is time to add backward edge
		// count - logaritmic complexity
		// at - logaritmic complexity

		if(residualGraph[to].count(from) > 0) { 
			residualGraph[to][from].second += bottleneck;
		} else {
			// cost(TO, FROM) = -cost(FROM, TO);

			residualGraph[to].emplace(from, CostCapacity(-cost, bottleneck));
		}

	}
}

int MaximumFlow(vector<unordered_map<int, CostCapacity>>& residualGraph, int source, int sink) {
	// vector<unordered_map<int, CostCapacity>> residualGraph = graph;  // create a residual graph

	int cost = 0;
	bool AugmentingPathLeft = true;
	while(AugmentingPathLeft) {
		AugmentingPath augPath = findAugmentingPath(residualGraph, source, sink);

		if(augPath.bottleneck > 0) {
			// augment
			augment(residualGraph, augPath);
			cost += augPath.cost;
		} else AugmentingPathLeft = false;
	}

	return cost;
}

bool cycle_find(vector<unordered_map<int, CostCapacity>>& residualGraph, int* pre) {
	vector<int> vec;
	bool on_stack[residualGraph.size()];
	bool visited[residualGraph.size()];

	for(int i=0; i<residualGraph.size(); i++) {
		on_stack[i] = false;
		visited[i] = false;
	}

	for(int i=0; i<residualGraph.size(); i++) 
		if(!visited[i]) {
			for(int j=i; j!= -1; j=pre[j]) 
				if(!visited[j]) {
					visited[j] = true;
					vec.push_back(j);
					on_stack[j] = true;
				}
				else {
					if(on_stack[j]) return true;
					break;
				}

			for(int j: vec) on_stack[j] = false;
			vec.clear();
	    }
	return false;
}

long augment_cycle(vector<unordered_map<int, CostCapacity>>& graph, int* pre, int v) {
	// NEGATIVE CYCLE - AUGMENT
	vector<int> aux;
	int in_vector[graph.size()];
	for(int i=0; i<graph.size(); i++) in_vector[i] = -1;

	int index = -1;
	                  
	while(in_vector[v] == -1) {
								
	aux.push_back(v);
	index++;
	in_vector[v] = index;
	v = pre[v];
								 
	}
	aux.push_back(v);
	

	int source = v;
	stack<int> path;
	int bottleneck = numeric_limits<int>::max();
	int cost = 0;

	for(int i=in_vector[source]; i<aux.size()-1; i++) {
		int to = aux[i];
		int from = aux[i+1];

		int capacity = graph[from][to].second;
		int currentCost = graph[from][to].first;
		if(bottleneck > capacity) bottleneck = capacity;

		cost += currentCost;
		path.push(to);

	}
							
	path.push(source);
	AugmentingPath aug(bottleneck, cost, path);
							
							
		augment(graph, aug);
		return cost;
							
}

void algorithm(vector<unordered_map<int, CostCapacity>>& graph, int* pre, int* dis, int* contains, queue<int>& q, int& minCost) {
	for(int v=graph.size() - 1; v>=0; v--) {
		q.push(v);
	}
	    int iteration = 0;
		while(!q.empty()) {

			int u = q.front();
			q.pop();
			contains[u] = false;
			bool changed = false;

			for(auto& pair: graph[u]) {
				if(changed) {
					if(!contains[u]) q.push(u);
					contains[u] = true;
					break;
				}

				int v = pair.first;
				int cost = pair.second.first;
				int capacity = pair.second.second;

				// weight(u, v) = cost
				// cout << u << " --> " << v << " now we are at start " << len[v] << endl;
				if(dis[u] + cost < dis[v]) {

					if(!contains[v]) {
						 q.push(v);
						contains[v] = true;
					}
					pre[v] = u;
					dis[v] = dis[u] + cost;
					iteration++;
					int check = v;

					// cout << u << " --> " <<  v << " now condition is satisfied " << len[v] << endl;
					// there is a negative cycle
					if(iteration == graph.size()) {
						iteration = 0;
						if(cycle_find(graph, pre)) {
							minCost += augment_cycle(graph, pre, v);
							changed = true;
						    for(int i=0; i<graph.size(); i++) pre[i] = -1;
						}
					}
				}
			}
		}
	}




int main(int argc, char* argv[]) {

	string infile_name = argv[1];
	string outfile_name = argv[2];

	ifstream infile;
	ofstream outfile;

	infile.open(infile_name);
	outfile.open(outfile_name);

	int T;
	infile >> T;


	// main for loop

	for(int i=0; i<T; i++) {
		int N, weight;
		infile >> N;

		vector<unordered_map<int, CostCapacity>> graph;
		// total nodes = 1 + 2N + 1  = 2N + 2
		for(int i=0; i<(2*N+2); i++) {
			graph.push_back(unordered_map<int, CostCapacity> ());
		}
		for(int j=1; j<=N; j++) {
			graph[0].emplace(j, CostCapacity(0, 1));
		}

		for(int j=1; j <= N; j++) {
			for(int k=N+1; k <= 2*N; k++) {
				infile >> weight;
				graph[j].emplace(k, CostCapacity(-weight, 1));
			}
			graph[j+N].emplace(2*N+1, CostCapacity(0, 1));
		}



	// First part --> Find maximum flow without considering costs
		int minCost = MaximumFlow(graph, 0, 2*N + 1);

	// inspired by <https://konaeakira.github.io/posts/using-the-shortest-path-faster-algorithm-to-find-negative-cycles.html>" 
	// negative cost cycles

		int dis[graph.size()];
		int pre[graph.size()];
		int contains[graph.size()];
		queue<int> q;

		for(int v=0; v<graph.size(); v++) {
			dis[v] = 0;
			pre[v] = -1;  // direct predecessor of v
			contains[v] = true;
		}

		algorithm(graph, pre, dis, contains, q, minCost);
		algorithm(graph, pre, dis, contains, q, minCost);

		outfile << -minCost << endl;
	}


	infile.close();
	outfile.close();

    return 0;
}
