## IE 310 Q6 ##
import math

# Do not run the code with functions that return extremely large values, otherwise it may give unexpected results

def f(x1, x2):
    return (5*x1 - x2)**4 + (x1 - 2)**2 + x1 - 2*x2 + 12

def f_a(a, x1, x2, d): # x1, x2 and d are constants
    x1 = x1 + a*d[0]
    x2 = x2 + a*d[1]
    return f(x1, x2)

# Calculate the length of the vector ||x||
def length(vector):
    return math.sqrt(sum([x**2 for x in vector]))

# Take derivative using limit definition
def derivative(f, x1, x2, i):
    delta = 0.0000000001
    if(i == 1):
        return (f(x1 + delta, x2) - f(x1, x2)) / delta
    else:  # if (i == 0)
        return (f(x1, x2 + delta) - f(x1, x2)) / delta
    
def gradient(f, x1, x2):
    return [derivative(f, x1, x2, 1), derivative(f, x1, x2, 2)]

def BisectionSearch(a, b, f, x1, x2, d, epsilon):
    x = 0
    itr = 0
    while(b - a >= epsilon):
        x = (a+b)/2
        if(f(x + epsilon, x1, x2, d) <= f(x, x1, x2, d)): a = x
        else: b = x
        itr += 1
    return x 

def SteepestDescent(f, epsilon):
    k = 0
    # choose a starting point
    x1 = 5
    x2 = 25
    while(length(gradient(f, x1, x2)) >= epsilon):
        d = [-m for m in gradient(f, x1, x2)]
        a = BisectionSearch(0, 20, f_a, x1, x2, d, epsilon)
        print("Iteration {:<2}: x1 = {:.4f} || x2 = {:.4f} || d[0] = {:^7.4f} || d[1] =  {:^7.4f} || a = {:.4f} || f(x1, x2) = {:.4f}".format(k, x1, x2, d[0], d[1], a, f(x1, x2)))
        x1 = x1 + a * d[0]
        x2 = x2 + a * d[1]
        k = k + 1

    return (x1, x2)

if __name__ == '__main__':  
    x1, x2 = SteepestDescent(f, 0.0001)
    print("Optimal solution -->  x1: {:.4f}, x2: {:.4f} || f(x): {:.4f}".format(x1, x2, f(x1, x2)))
