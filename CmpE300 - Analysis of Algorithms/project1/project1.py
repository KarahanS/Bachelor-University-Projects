import random
import datetime

def func(X, n):
    y = 0
    for i in range(n):
        if(X[i] == 0):
            for j in range(i, n):
                k = n
                while(k >= 1):
                    y = y + 1
                    k = k // 2
        else:
            for m in range(i, n):
                for t in range(1, n + 1):
                    x = n
                    while(x>0):
                        x = x - t
                        y = y + 1
    return y


def average():
    
    prob = [0, 1, 1]
    input_size = [1, 10, 50, 100, 200, 300, 400, 500, 600, 700]
    
    for N in input_size:
        list_ = []    
        for n in range(N):
            list_.append(prob[random.randint(0, 2)])
        
        results = []
        for i in range(3):
            start = datetime.datetime.now()
            func(list_, N) 
            end = datetime.datetime.now()
            delta = end - start
            mill = (delta.total_seconds()) * 1000
            results.append(mill)
        
        print("Case: Average".ljust(20), end = "")
        print("Size: {}".format(N).ljust(15), end = "")
        print("Elapsed Time: %.3f milliseconds".ljust(15) %(sum(results) / 3))

    
def worst():
    
    input_size = [1, 10, 50, 100, 200, 300, 400, 500, 600, 700]
    
    for N in input_size:
        list_ = []    
        for n in range(N):  
            list_.append(1)  # assume always X[i] = 1 
        
        start = datetime.datetime.now()
        func(list_, N) 
        end = datetime.datetime.now()
        delta = end - start
        mill = (delta.total_seconds()) * 1000
            
        print("Case: Worst".ljust(15), end = "")
        print("Size: {}".format(N).ljust(15), end = "")
        print("Elapsed Time: %.3f milliseconds".ljust(15) %(mill))
    
def best():
    
    input_size = [1, 10, 50, 100, 200, 300, 400, 500, 600, 700]
    
    for N in input_size:
        list_ = []    
        for n in range(N):  
            list_.append(0)  # assume always X[i] = 0 
        
        start = datetime.datetime.now()
        func(list_, N) 
        end = datetime.datetime.now()
        delta = end - start
        mill = (delta.total_seconds()) * 1000    
        print("Case: Best".ljust(15), end = "")
        print("Size: {}".format(N).ljust(15), end = "")
        print("Elapsed Time: %.3f milliseconds".ljust(15) %(mill))
        
        #print("Case: Best", "Size: {}".format(N), "Elapsed Time: %.3f milliseconds" %(mill))

if __name__ == '__main__':
    average()
    worst()
    best()
    