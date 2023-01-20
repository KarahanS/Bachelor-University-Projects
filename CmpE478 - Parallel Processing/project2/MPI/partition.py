import time
import metis
import networkx as nx

#comm = MPI.COMM_WORLD
#size = comm.Get_size()  # number of processors (manager + workers)
#rank = comm.Get_rank()  # which process (rank=0 --> manager process)
#workers = size - 1     # number of workers
#if(workers <= 1):
#    print("Metis needs at least 2 worker processors to partition the graph.")
#    exit(1)

hashmap = dict()    # stores (website, i) pairs
indices = dict()    # indices[i] = website  (reverse)
adj = dict()        # adj[i] = [j, k] --> there is a link from j to i, from k to i.
G = nx.Graph()      # graph (undirected)
outdegree = dict()  # number of outgoing edges from a node  outdegree[i] = 4  (4 edges from i)
idx = 0

# CSR data structures
row_begin = []
values = []
col_indices = []

# constants
ALPHA = 0.2
EPSILON = 1e-6

def toCSR(file):
    global idx, adj, hashmap, indices, outdegree
    print("File reading starts now...")
    start = time.time()
    fh = open(file, "r")
    for line in fh:
        fr, to = line.strip().split()  # get rid of '\n' and split by '\t'

        f = 0
        t = 0

        if fr not in hashmap:
            hashmap[fr] = idx
            indices[idx] = fr
            f = idx
            idx = idx + 1
        else:
            f = hashmap[fr]
        
        if to not in hashmap:
            hashmap[to] = idx
            indices[idx] = to
            t = idx
            idx = idx + 1
        else:
            t = hashmap[to]
        
        if f not in adj: 
            adj[f] = []  # list
            G.add_node(f)
        if t not in adj: 
            adj[t] = []  # list
            G.add_node(t)

        # we want Q_ij to be marked if there is a link from j(th) page to i(th) page.
        adj[t].append(f)
        G.add_edge(f, t)

        if(f not in outdegree): outdegree[f] = 1
        else: outdegree[f] += 1

    fh.close()


def main():
    toCSR("../graph.txt")
    for i in [7, 8, 9, 15, 20]:
        print("Metis partitioning starts now...")
        metis_start = time.time()
        workers = i
        print("workers:", workers)
        (edgecuts, parts) = metis.part_graph(G, workers)
        metis_end = time.time()
        w = open("partitions/p{}.txt".format(i), "a")
        for idx in range(len(parts)):
            node = indices[idx]
            part = parts[idx]
            w.write(node + "\t" + str(part) + "\n")

        w.close()
        print(round(metis_end - metis_start, 2), "seconds have passed for Metis partitioning.")


        row_begin.append(0)
        for i in range(len(adj)):
            row_begin.append(row_begin[-1] + len(adj[i]))
            for j in range(len(adj[i])):
                col_indices.append(adj[i][j])

        N = len(row_begin) - 1
        for i in range(N):
            for j in range(row_begin[i], row_begin[i + 1]):
                fr = col_indices[j]  # website T_i which has a citation to our website A
                outd = outdegree[fr] # calculate C_i of the website (outdegree)
                values.append(1/outd)
        
        end = time.time()

    # distribute graph to workers

if __name__ == "__main__":
    main()