SIZE = 512

def matmul(C, A, B):
    for i in range(SIZE):
        for j in range(SIZE): 
            for k in range(SIZE): 
                C[i][j] += A[i][k] * B[k][j]
              
if __name__ == "__main__":

    # init
    A = [[ i*j+i+1 for j in range(SIZE) ] for i in range(SIZE) ]
    B = [[ i*j+i+2 for j in range(SIZE) ] for i in range(SIZE) ]
    C = [[ 0 for i in range(SIZE) ] for j in range(SIZE) ]
  
    # core
    matmul(C, A, B)

    # print(C)

