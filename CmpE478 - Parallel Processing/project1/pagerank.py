import networkx as nx
import numpy as np

G_tmp = nx.read_edgelist('graph.txt', create_using = nx.DiGraph)
c = sorted(nx.weakly_connected_components(G_tmp), key=len, reverse=True)
wcc_set = c[0]
G = G_tmp.subgraph(wcc_set)

truth = nx.pagerank(G, alpha=0.2, max_iter = 100, tol=1e-06)
truth = {k: v for k, v in sorted(truth.items(), key=lambda item: item[1], reverse=True)}
print("part of networkx's result\n", list(truth.keys())[:5])