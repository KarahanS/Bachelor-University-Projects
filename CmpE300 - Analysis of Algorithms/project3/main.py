from random import randrange

# chess = NxN board
# n = boardsize
# C = column (of the queen)
# R = current row
def updateChessboard(chess, n, C, R): 
    # update the chessBoard
    
    # vertical
    for i in range(n):
        chess[i][C] = False
            
    # diagonal - [R][C]
    # from upper-left to lower-right
    a = R - min(R, C)
    b = C - min(R, C)
    while(a < n and b < n):
        chess[a][b] = False
        a += 1
        b += 1
        
    # from lower-left to upper-right
    a = R + min(n - 1 - R, C)
    b = C - min(n - 1 - R, C)
    while(a >= 0 and b < n):
        chess[a][b] = False
        a -= 1
        b += 1
    
    return chess

# n = boardsize
# f = file to write into
def QueensLasVegas(n, f):
    Column = [None for i in range(n)] 
    AvailColumns = [i for i in range(n)]
    chess = [[True for _ in range(n)] for _ in range(n)]
    R = 0
    step = 1
    while(len(AvailColumns) != 0 and R <= n - 1):
        # Randomly pick an available column
        C = AvailColumns[randrange(len(AvailColumns))]
        Column[R] = C  
        
        # update the chessboard
        chess = updateChessboard(chess, n, C, R)
        R += 1 
        
        # update the available columns
        if(R != n): AvailColumns = [i for i in range(n) if chess[R][i]]   
        else: AvailColumns = []
        
        # write the results to the file
        f.write("Step {}: Columns: {}\n".format(step, [x for x in Column if x is not None]))
        f.write("Step {}: Available: {}\n".format(step, AvailColumns))
        step += 1
    return Column

def part1():
    n_list = [6, 8, 10]
    for n in n_list:
        f = open("results_{}.txt".format(n), "a")
        print("LasVegas Algorithm With n = {}".format(n))
        success = 0
        failure = 0
        N = 10000
        for i in range(N):
            k = QueensLasVegas(n, f)
            if None in k: 
                f.write("Unsuccessful\n")
                failure += 1
            else: 
                f.write("Successful\n")
                success += 1
        print("Number of successful placements is {}".format(success))
        print("Number of trials is {}".format(N))
        print("Probability that it will come to a solution is {}".format(success / N))
        f.close()
        
# n = boardsize
# k = number of randomly placed queens
def QueensLasVegas2(n, k):
    Column = [None for i in range(n)] 
    AvailColumns = [i for i in range(n)]
    chess = [[True for _ in range(n)] for _ in range(n)]
    R = 0
    
    # probabilistic part
    while(True):
        while(len(AvailColumns) != 0 and R < k):
            C = AvailColumns[randrange(len(AvailColumns))]
            Column[R] = C 
        
            # update the chessboard
            chess = updateChessboard(chess, n, C, R)
            R += 1 
        
            # prepare AvailColumns for the (R+1)th queen in row R+1
            if(R != n): AvailColumns = [i for i in range(n) if chess[R][i]]   
            else: AvailColumns = []
        
        if(R == k): break
        # probabilistic part may have already stuck in dead-end
        else:
            R = 0
            AvailColumns = [i for i in range(n)]
            Column = [None for i in range(n)] 
            chess = [[True for _ in range(n)] for _ in range(n)]

    # although k queens are placed, it may be dead-end.
    if(len(AvailColumns) == 0): return Column
    
    # copy the chessboard and other lists, append to stack
    copy = [row[:] for row in chess]
    stack = [(list(AvailColumns), list(Column), copy)]  
    
    while(len(stack) != 0 and R < n):
        if(len(AvailColumns) != 0): 
            copy = [row[:] for row in chess]
            stack.append((list(AvailColumns), list(Column), copy))
            
            C = AvailColumns[-1] 
            Column[R] = C
            # update the chessboard
            chess = updateChessboard(chess, n, C, R)
        
            R += 1
            if(R != n): AvailColumns = [i for i in range(n) if chess[R][i]]   
            else: AvailColumns = []
        else:  
            # Pop the previous state from the stack
            previousState = stack.pop()
            AvailColumns = previousState[0]
            Columns = previousState[1]
            chess = previousState[2]
            
            # Pop the previously selected column, it leads to dead end
            AvailColumns.pop()
            R -= 1  
    return Column

def part2():
    n_list = [6, 8, 10]
    for n in n_list:
        print("\n---------------------{}---------------------".format(n))
        for k in range(n):
            success = 0
            failure = 0
            N = 10000
            for i in range(N):
                out = QueensLasVegas2(n, k)
                if None in out: failure += 1
                else: success += 1
            print("k is {}".format(k))
            print("Number of successful placements is {}".format(success))
            print("Number of trials is {}".format(N))
            print("Probability that it will come to a solution is {}".format(success / N))
                
if __name__ == '__main__':  
    arg = input()
    if(arg == 'part1'):
        part1()
    elif(arg == 'part2'):
        part2()
    else:
        print("Invalid input. It should be either 'part1' or 'part2'.")