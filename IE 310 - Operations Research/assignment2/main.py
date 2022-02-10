UNIQUE = False
ARBITRARY = False

def isZero(num):
    allowed_error = 0.00001
    return abs(num - 0) <= allowed_error

def interchange_row(matrix, rowA, rowB):
    matrix[rowA], matrix[rowB] = matrix[rowB], matrix[rowA]

def multiply_row(matrix, row, c):
    matrix[row] = [x * c for x in matrix[row]]

def identity_matrix(n):
    identity = []
    for i in range(n):
        identity.append([0 if j != i else 1 for j in range(n)])
    return identity

def Gauss_Jordan(mat, augmented = False):  # augmented = A|b
    matrix = [row[:] for row in mat]
    n = len(matrix[0]) - 1 if augmented else len(matrix[0])
    for column in range(n):
        for row in range(column, len(matrix)):   # for each column, check the rows to find a pivot
            if(not isZero(matrix[row][column])):
                # swap this row with the n(th) row. n = index of column
                pivot_row = column
                interchange_row(matrix, pivot_row, row)
                c = 1 / matrix[pivot_row][column]
                multiply_row(matrix, pivot_row, c) # multiply pivot row with 1 / pivot to make value of pivot equal to 1.
                # now, substract this row from all rows
                for r in range(len(matrix)):
                    matrix[r] = [a - b * (matrix[r][column])if r != pivot_row else a for a, b in zip(matrix[r], matrix[pivot_row])]
            else: matrix[row][column] = 0
    return matrix

def inverse_matrix(mat):
    matrix = [row[:] for row in mat]
    n = len(matrix[0])
    identity = identity_matrix(n)
    for column in range(n):
        for row in range(column, len(matrix)):
            if(not isZero(matrix[row][column])):
                pivot_row = column
                interchange_row(matrix, pivot_row, row)
                interchange_row(identity, pivot_row, row)
                c = 1 / matrix[pivot_row][column]
                multiply_row(matrix, pivot_row, c)
                multiply_row(identity, pivot_row, c)
                for r in range(len(matrix)):
                    val = matrix[r][column]
                    matrix[r] = [a - b * val if r != pivot_row else a for a, b in zip(matrix[r], matrix[pivot_row])]
                    identity[r] = [a - b * val if r != pivot_row else a for a, b in zip(identity[r], identity[pivot_row])]
            else: matrix[row][column] = 0
    return identity

def solve(matrix, b):
    A = Gauss_Jordan(matrix)
    m = [row[:] for row in matrix]
    for r, b_ in zip(matrix, b):
        r.append(b_)
    Ab = Gauss_Jordan(matrix, augmented=True)
    n = len(matrix)
    rank_A = rank(A)
    rank_Ab = rank(Ab)

    if (rank_A == n):
        sol = {}
        for r in range(len(Ab)): sol['x{}'.format(r+1)] = Ab[r][-1]
        inverse = inverse_matrix(m)
        global UNIQUE
        UNIQUE = True
        return (sol, inverse)
    elif(rank_A == rank_Ab):
        arbitrary = []
        sol = {}
        for r in range(len(Ab)):
            if(Ab[r][r] != 0): sol['x{}'.format(r+1)] = Ab[r][-1]
            else:
                sol['x{}'.format(r+1)] = 0
                arbitrary.append(r+1)
        global ARBITRARY
        ARBITRARY = True
        return (sol, arbitrary)
    else:
        return -1

def rank(matrix):
    rank = 0
    for row in matrix:
        rank = rank + 1 if sum(row) != 0 else rank
    return rank 

def main(filename):
    print("#"*50)
    print("Output for the file", filename)
    global UNIQUE
    global ARBITRARY
    with open(filename,'r',encoding = 'utf-8') as f:
        lines = f.readlines()
        n = int(lines[0].replace("\n",""))
        A = []
        b = []
        for i in range(n):
            row =  [float(x) for x in  lines[i + 1].replace("\n","").split()] 
            A.append(row[:-1])
            b.append(row[-1])
        
        solution = solve(A, b)
        if(UNIQUE):
            sol = ['{} = {:.2f}'.format(x, y) for x, y in solution[0].items()]
            inverse = solution[1]
            print("Unique solution:", ", ".join(sol))
            print("Inverted A: ", end="")

            inverse[0] =  ['{:.2f}'.format(x) for x in inverse[0]]
            print(" ".join(inverse[0]))

            for i in range(1, len(inverse)):
                inverse[i] =  ['{:.2f}'.format(x) for x in inverse[i]]
                print("\t   ", " ".join(inverse[i]))
        elif(ARBITRARY):
            sol = ['{} = {:.2f}'.format(x, y) for x, y in solution[0].items()]
            arbitrary = ['{} = {:.2f}'.format("x{}".format(x), solution[0]["x{}".format(x)]) for x in solution[1]]
            print("Arbitrary variables:", ", ".join(arbitrary))
            print("Arbitrary solution:", ", ".join(sol))

        else:  # INCONSISTENT
            print("Inconsistent problem")
    
    print("#"*50)
    UNIQUE = False
    ARBITRARY = False

    
if __name__ == '__main__':
    """ 
    Expected output for test1.txt:
    Unique solution: 1.0 2.0 3.0
    Inverted A: 1.00 2.00 -1.00
                0.50 -0.50 0.00
                -0.50 -1.50 1.00

    Expected output for test2.txt:
    Inconsistent problem

    Expected output for test3.txt:
    Arbitrary variables: 0.00
    Arbitrary solution: -8.00 0.00 -6.00

    Output for the file Data1.txt:
    Arbitrary variables: x3 = 0.00
    Arbitrary solution: x1 = 6.60, x2 = 1.80, x3 = 0.00  

    Output for the file Data2.txt:
    Unique solution: x1 = 1.00, x2 = -0.50, x3 = 1.50    
    Inverted A: 0.50 0.17 0.33
                1.00 0.40 0.20
                0.00 0.13 0.07

    Output for the file Data3.txt:
    Inconsistent problem

    Output for the file Data4.txt:
    Unique solution: x1 = 1.60, x2 = 0.28, x3 = 0.77, x4 = -0.69, x5 = 0.97, x6 = -1.04
    Inverted A: 0.21 -0.09 0.04 0.05 -0.05 -0.16
                -0.00 -0.05 -0.04 0.10 -0.07 0.17
                -0.05 -0.03 0.07 -0.03 0.09 -0.06
                -0.07 0.09 -0.02 -0.03 -0.04 0.08
                0.08 -0.06 -0.03 0.03 -0.01 0.05
                -0.14 0.12 -0.02 -0.07 0.07 -0.02
    """
    main("test1.txt")
    main("test2.txt")
    main("test3.txt")
    main("Data1.txt")
    main("Data2.txt")
    main("Data3.txt")
    main("Data4.txt")
    # main("input.txt")