N = 20
TELEPORTATION_RATE = 0.10
EPSILON = 1e-6

def construct_pmatrix(vertices, edges):
    prob_matrix = []
    for i in range(len(vertices)):
        prob_matrix.append([])
        for j in range(len(vertices)):
            prob_matrix[i].append(0)
    
    # len(prob_matrix) = 459 
    for i in range(len(edges)):
        for j in range(len(edges[i])):
            prob_matrix[i][edges[i][j]] = 1.0 / len(edges[i])
        
        if(len(edges[i]) == 0):
            print("vertex {name} has no outgoing edges".format(name = vertices[i]))

    # prob_matrix[i][j] = 1 / len(edges[i]) if j in edges[i]
    # prob_matrix[i][j] = 0 if j not in edges[i]

    # add teleportation to each destination
    for i in range(len(prob_matrix)):
        for j in range(len(prob_matrix[i])):
            prob_matrix[i][j] = prob_matrix[i][j] * (1 - TELEPORTATION_RATE) + TELEPORTATION_RATE / len(prob_matrix[i])

    return prob_matrix

# prob_matrix[i][j] = probability of going from vertex i to vertex j
def power_iteration(prob_matrix):
    # initialize the vector
    v0 = []
    for i in range(len(prob_matrix)):
        v0.append(1.0 / len(prob_matrix))
    
    itr = 0
    while(True):
        itr+=1
        v1 = []
        for i in range(len(prob_matrix)):
            v1.append(0)
            for j in range(len(prob_matrix)):
                v1[i] += prob_matrix[j][i] * v0[j]
        
        l1 = 0
        for i in range(len(v1)):
            l1 += abs(v1[i] - v0[i])
        if(l1 < EPSILON): break
        v0 = v1.copy()
    print("Number of iterations:", itr)
    return v1

def pagerank(vertices, edges): 
    prob_matrix = construct_pmatrix(vertices, edges)
    return power_iteration(prob_matrix)
    
if __name__ == '__main__':
    # read the data.txt vertices and edges
    vertices = {}
    edges = []

    with open('data.txt', 'r') as f:
        fline = f.readline()
        num_vertices = int(fline.strip().split()[1])

        for i in range(num_vertices):
            vertex = f.readline().strip().split()
            vertices[int(vertex[0]) - 1] = vertex[1].replace('"', '')
        
        for _ in range(num_vertices):
            edges.append([])

        f.readline() # consume "edges" line
        # read the edges
        for line in f:
            edge = line.strip().split()

            e0 = int(edge[0]) - 1
            e1 = int(edge[1]) - 1

            if e1 in edges[e0]: continue
            edges[e0].append(e1)
            edges[e1].append(e0)

    # vertices[index] = name
    # edges[index] = [v1, v2, ...] (list of vertices connected to vertex with ID = index)
            
    res = pagerank(vertices, edges)  
    assert N <= len(res)
    topn = {}

    # normalize res
    norm_constant = 1.0 / sum(res)
    for i in range(len(res)):
        res[i] *= norm_constant  
  
    for i in range(N):
        id = res.index(max(res))
        topn[id] = res[id]
        res[id] = -1 # eliminate the max value

    for id in topn:
        print("{name} --> {prob}".format(name = vertices[id], prob = format(topn[id], '.2e')))
