## IE 310 Q5 ##
import math

def f(x):
    return (10 + 0.01 * x - 0.1 * x**2 + 0.8 * math.cos(3 * x))

# b > a
def BisectionSearch(a, b, f, epsilon):
    x = 0
    itr = 0
    while(b - a >= epsilon):
        x = (a+b)/2
        print("Iteration {:<2}: x = {:.8f} || f(x) = {:.8f} || f(x + e) = {:.8f} || a = {:.8f} || b = {:.8f}".format(itr, x, f(x), f(x + epsilon), a, b))
        if(f(x + epsilon) <= f(x)): a = x
        else: b = x
        itr += 1
    return x 

if __name__ == '__main__':
    subintervals = [(-3.655, -2.627), (-1.562, -0.533), (0.533, 1.562), (2.627, 3.655)]
    globalMin = 0
    for subinterval in subintervals:
        print("Subinterval : {}".format(subinterval))
        localmin = BisectionSearch(subinterval[0], subinterval[1], f, epsilon = 0.0001)
        print("BisectionSearch has finished.")
        if(f(localmin) < f(globalMin)):
            globalMin = localmin
    left = f(-4)
    right = f(4)
    if(left < f(globalMin)): globalMin = -4
    if(right < f(globalMin)): globalMin = 4
    
    print("Optimal solution -->  x: {:.5f} || f(x): {:.5f}".format(globalMin, f(globalMin)))