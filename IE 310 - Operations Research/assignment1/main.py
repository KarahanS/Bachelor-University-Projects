def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))] 

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def Gauss_Jordan(matrix):
    pivots = [] # rows
    for col in range(len(matrix[0])):
        pivot = None
        for row in range(len(matrix)):
            if(matrix[row][col] != 0 and row not in pivots):
                pivot = row
                break
        if(pivot is None): continue  # no pivot for this column
        pivots.append(pivot)

        # now we found a candidate pivot
        p = matrix[row][col]
        matrix[row] = [x / p for x in matrix[row]]
        for r in range(len(matrix)):
            matrix[r] = [a - b * (matrix[r][col])if r != row else a for a, b in zip(matrix[r], matrix[row])]

    return matrix

def adjust(matrix, columns, variables):
    cols = []
    for i in range(len(variables)):
        if(variables[i] is None): cols.append(columns[i])
    for c in columns:
        if c not in cols: cols.append(c)
    matrix = [[cols[j][i] for j in range(len(cols))] for i in range(len(cols[0]))] 
    return Gauss_Jordan(matrix)

def solve_matrix(matrix, columns, variables):
    matrix = adjust(matrix, columns, variables)
    idx = 0
    for i in range(len(variables)):
        if(variables[i] is None):
            variables[i] = matrix[idx][-1] / matrix[idx][idx] if matrix[idx][idx]  != 0 else 0
            idx += 1
    return variables

def __solve(obj, st_coef, st_cons, matrix):
    allowed_error = 0.00001
    sol = None
    solutionSet = None
    columns = transpose(matrix)
    for comb in combinations([i for i in range(len(matrix[0]) - 1)], len(matrix[0]) - 1 - len(matrix)): # select non-basics
        variables = [0 if c in comb else None for c in range(len(matrix[0]) - 1)]
        variables = solve_matrix(matrix, columns, variables)
        valid = not(any([variables[i] + allowed_error < 0 for i in range(len(variables))]))

        if(valid and validate(st_coef, st_cons, variables)):
            total = get_total(obj, variables)
            if(sol is None or (total < sol and obj[-1] == "min") or (total > sol and obj[-1] == "max")): 
                sol = total
                solutionSet = [var for var in variables[:len(obj) - 1]]  
    return (sol, solutionSet)

def validate(st_coef, st_cons, variables):
    allowed_error = 0.00001
    for constraint, limit in zip(st_coef, st_cons):
        total = sum([a * b for a,b in zip(constraint[:-1], variables)])
        if(constraint[-1] == "<="): boo = total <= limit +  allowed_error
        elif(constraint[-1] == ">="): boo = total + allowed_error >= limit
        else: boo = abs(total - limit) <= allowed_error
        
        if(not boo): return False
    return True

def get_total(obj, variables):
    total = sum([a * b for a,b in zip(obj[:-1], variables)])  # length of variables can be longer than obj - slack variables
    return total

def create_matrix(st_coef, st_cons):
    matrix = []
    cnt = 0
    for i in st_coef: cnt = cnt + 1 if i[-1] == "<=" or i[-1] == ">=" else cnt
    slack = {"<=":1, "=":0, ">=":-1}
    c = 0

    for a, b in zip(st_coef, st_cons):
        slackvar = [0]*cnt
        slackvar[c] = slack[a[-1]]       
        matrix += [a[:-1] + slackvar + [b]]
        if(a[-1] != "="): c+=1
    
    return matrix

def solve(obj, st_coef, st_cons):
    matrix = create_matrix(st_coef, st_cons)
    return __solve(obj, st_coef, st_cons, matrix)

def integer_solutionA(tpl, st_coef, st_cons):
    rng = 5
    variables = tpl[1]
    sol = None
    solutionSet = None

    a = round(variables[0])
    b = round(variables[1])
    c = round(variables[2])
    d = round(variables[3])
    for a_ in range(a - rng, a + rng):
        for b_ in range(b - rng, b + rng):
            for c_ in range(c - rng, c + rng):
                for d_ in range(d - rng, d + rng):
                    variables = [a_, b_, c_, d_]
                    valid = not(any([variables[i] < 0 for i in range(len(variables))]))
                    if(valid and validate(st_coef, st_cons, variables)):
                        total = get_total(obj, variables)
                        if(sol is None or (total < sol and obj[-1] == "min") or (total > sol and obj[-1] == "max")): 
                            sol = total
                            solutionSet = [var for var in variables[:len(obj) - 1]]  
    return sol, solutionSet

def integer_solutionB(tpl, st_coef, st_cons):
    rng = 15
    variables = tpl[1]
    sol = None
    solutionSet = None

    a = round(variables[0])
    b = round(variables[1])
    c = round(variables[2])
    d = round(variables[3])
    e = round(variables[4])
    for a_ in range(a - rng, a + rng):
        for b_ in range(b - rng, b + rng):
            for c_ in range(c - rng, c + rng):
                for d_ in range(d - rng, d + rng):
                    for e_ in range(e - rng, e + rng):
                        variables = [a_, b_, c_, d_, e_]
                        valid = not(any([variables[i] < 0 for i in range(len(variables))]))
                        if(valid and validate(st_coef, st_cons, variables)):
                            total = get_total(obj, variables)
                            if(sol is None or (total < sol and obj[-1] == "min") or (total > sol and obj[-1] == "max")): 
                                sol = total
                                solutionSet = [var for var in variables[:len(obj) - 1]]  
    return sol, solutionSet

def brute_forceA(st_coef, st_cons, obj):
    sol = None
    solutionSet = None

    for a in range(0, 31):
        for b in range(0, 31):
            for c in range(0, 31):
                for d in range(0, 31):
                    variables = [a, b, c, d]
                    if(validate(st_coef, st_cons, variables)):
                        total = get_total(obj, variables)
                        if(sol is None or (total < sol and obj[-1] == "min") or (total > sol and obj[-1] == "max")): 
                            sol = total
                            solutionSet = [var for var in variables[:len(obj) - 1]]  
    return sol, solutionSet

def brute_forceB(st_coef, st_cons, obj):
    sol = None
    solutionSet = None

    for a in range(0, 31):
        for b in range(0, 31):
            for c in range(0, 31):
                for d in range(0, 31):
                    for e in range(0, 201):
                        variables = [a, b, c, d, e]
                        if(validate(st_coef, st_cons, variables)):
                            total = get_total(obj, variables)
                            if(sol is None or (total < sol and obj[-1] == "min") or (total > sol and obj[-1] == "max")): 
                                sol = total
                                solutionSet = [var for var in variables[:len(obj) - 1]]  
    return sol, solutionSet

"""
###  6th question ###
obj = [10, 20, "max"]
st_coef = [[-1, 2, "<="],
           [1, 1, "<="],
           [5, 3, "<="]]
st_cons = [15, 12, 45]                    
"""

"""
Test #1 = (90.66666666666667, [3.7777777777777777, 3.4444444444444446, 13.11111111111111])
obj = [3, 4, 5, "max"]
st_coef = [[2, 1, 0, "<="],
            [0, 2, 1, "<="],
            [1, 0, 2, "<="]]
st_cons = [11, 20, 30]
"""

"""
       Part (B) - Overtime
obj = [690, 545, 1020, 785, 30,  "min"]
st_coef = [[20, 30, 10, 25, -1,  "<="],
               [160, 100, 200, 75, 0, "<="],
               [30, 35, 60, 80, 0, "<="],
               [35, 45, 70, 0, 0, ">="],
               [55, 42, 0, 90, 0, ">="]]
st_cons = [1000, 8000, 4000, 2100, 1800]

"""

obj = [690, 545, 1020, 785, 30,  "min"]
st_coef = [[20, 30, 10, 25, -1,  "<="],
               [160, 100, 200, 75, 0, "<="],
               [30, 35, 60, 80, 0, "<="],
               [35, 45, 70, 0, 0, ">="],
               [55, 42, 0, 90, 0, ">="]]
st_cons = [1000, 8000, 4000, 2100, 1800]



###  Get optimal solution  (real numbers) ###
print(solve(obj, st_coef, st_cons))

### Solve part A using brute force ###
# print(brute_forceA(st_coef, st_cons, obj))

### Solve part B using brute force ###
# print(brute_forceB(st_coef, st_cons, obj))

### Solve part A using optimized solution
# tpl = solve(obj, st_coef, st_cons)
# print(integer_solutionA(tpl, st_coef, st_cons))

### Solve part B using optimized solution
tpl = solve(obj, st_coef, st_cons)
print(integer_solutionB(tpl, st_coef, st_cons))
