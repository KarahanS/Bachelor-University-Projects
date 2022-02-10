#### CmpE343 Assignment II ####
import numpy as np
import matplotlib.pyplot as plt

#### CmpE343 Assignment II ####
def p1():
    path_to_data = "benan.npy"
    data = np.load(path_to_data)

    n = len(data)
    print("Sample size: {}".format(n))

    # find sample mean
    mean = sum(data) / n
    print("Mean of the sample: {}".format(mean))

    # find sample variance
    sample_variance = sum([(xi - mean)**2 for xi in data]) / (n - 1)
    print("Variance of the sample: {}".format(sample_variance))


def p4_b():
    #### part b ####
    # Actual result: P(0 <= Z <= 1) : P(Z <= 1) - P(Z <= 0) = 0.8413 - 0.5000 = 0.3413
    sample_sizes = [10, 100, 1000, 10000, 100000, 1000000, 10000000]  # takes some time for the last one
    estimated_probabilities = []
    for size in sample_sizes:
        normal = np.random.normal(0, 1, size)
        cnt = 0
        for n in normal: 
            if(n <= 1 and n >= 0): cnt += 1
        print("Estimated probability: {:.4f} with size {}".format(cnt / size, size))
        estimated_probabilities.append(cnt/size)
        
    plt.title('Results of the Monte Carlo Simulation')
    plt.plot(sample_sizes, estimated_probabilities)
    plt.ylim(0.3413 - 0.25, 0.3413 + 0.25)
    plt.xscale('log')
    plt.ylabel('Estimated Probability')
    plt.xlabel('Sample size')
    plt.show()    

def p4_c():
    sample_sizes = [10, 100, 200, 300, 1000, 10000, 100000, 1000000, 10000000] 
    k_list = [2, 5, 10]
    for k in k_list:
        RHS = 1 / k**2
        e = k*1  # k*sigma   # P(|X| >= e) <= RHS
        print("Right hand side of the inequality = {}".format(RHS))
        estimations = []
        for size in sample_sizes:
            normal = np.random.normal(0, 1, size)
            cnt = 0
            for n in normal:
                if(abs(n) >= e): cnt += 1
            prob = cnt / size
            print("Estimated probability : {:.4f} with size {}".format(prob, size))
            estimations.append(prob)
        
        plt.title('Plot for k = {}'.format(k))
        plt.plot(sample_sizes, [RHS]*len(sample_sizes), 'r--')
        plt.plot(sample_sizes, estimations)
        plt.ylim(RHS - 0.5, RHS + 0.5)
        plt.xscale('log')
        plt.ylabel('Estimated probability values')
        plt.xlabel('Sample size')
        plt.show()
        
def p4_a():
    a = 0
    b = np.pi
    
    results = []
    sample_sizes =  [1000, 2000, 3000, 10000, 20000, 30000, 40000, 50000,
                     100000, 200000, 300000, 1000000, 2000000, 3000000, 4000000, 5000000]
    for size in sample_sizes:
        u = np.random.uniform(a, b, size)
        sum_ = 0
        
        for el in u:
            sum_ += np.cos(el)
        
        res = (b - a)/size * sum_
        print("Estimated value of the integration: {:.4f} with sample size {}".format(res, size))
        results.append(res)
        
    plt.title('Results of the Monte Carlo Simulation')
    plt.plot(sample_sizes, results)
    plt.ylim(0 - 0.25, 0 + 0.25)
    plt.xscale('log')
    plt.ylabel('Area')
    plt.xlabel('Sample size')
    plt.show()
    
    print("It can be seen from the graph that as sample size increases, result becomes closer and closer to zero, the expected result.")

def LCG(X, a, c, m):
    return (a * X + c) % m

# Linear Congruential Generator
# These are the constant a, c and modulo values used in MMIX by Donald Knuth
def p3_a(n, X):
    sample = []
    for i in range(n):
        X = LCG(X, a=6364136223846793005, c=1442695040888963407, m=2**64)
        sample.append(X/(2**64))
    return sample

def Z1(u1, u2):
    return np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
def Z2(u1, u2):
    return np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)

def p3_b():
    LCG = p3_a(20000, 0)
    sample1 = LCG[0:10000]
    sample2 = LCG[10000:200000]

    sampleZ1 = []
    sampleZ2 = []
    for u1, u2 in zip(sample1, sample2):
        sampleZ1.append(Z1(u1, u2))
        sampleZ2.append(Z2(u1, u2))
        
    plt.hist(sampleZ1, bins = 500, color = "skyblue")
    plt.title("Normal Distribution - Linear Congruential Generator")
    plt.xlabel("Z1")
    plt.ylabel("Frequency")
    plt.show()
    plt.hist(sampleZ2, bins = 500, color = "skyblue")
    plt.title("Normal Distribution - Linear Congruential Generator")
    plt.xlabel("Z2")
    plt.ylabel("Frequency")
    plt.show()
    return (sampleZ1, sampleZ2)
    
if __name__ == '__main__':
    ### Problem 1 ###
    #p1()
    
    ### Problem 3 - A ###
    
    LCG1, LCG2 = p3_b()

    sample1 = np.random.rand(10000)
    sample2 = np.random.rand(10000)
    sampleZ1 = []
    sampleZ2 = []
    for u1, u2 in zip(sample1, sample2):
        sampleZ1.append(Z1(u1, u2))
        sampleZ2.append(Z2(u1, u2))    
    
    # Independent Histograms    
    plt.hist(sampleZ1, bins = 500)
    plt.title("Normal Distribution - Prebuilt Generator")
    plt.xlabel("Z1")
    plt.ylabel("Frequency")
    plt.show()
    plt.hist(sampleZ2, bins = 500)
    plt.title("Normal Distribution - Prebuilt Generator")
    plt.xlabel("Z2")
    plt.ylabel("Frequency")
    plt.show()
    
    # SuperImposed Histograms
    plt.hist([sampleZ1, LCG1], alpha=0.5,bins = 200, label=['Prebuilt Generator', 'LCG'])
    plt.title("Prebuilt Generator - LCG Results Combined")
    plt.xlabel("Z1")
    plt.ylabel("Frequency")
    plt.legend(loc='upper right')
    plt.show()
    
    plt.hist([sampleZ2, LCG2], alpha=0.5,bins = 200, label=['Prebuilt Generator', 'LCG'])
    plt.title("Prebuilt Generator - LCG Results Combined")
    plt.xlabel("Z2")
    plt.ylabel("Frequency")
    plt.legend(loc='upper right')
    plt.show()
             
    ### Problem 4 - A ###
    p4_a()
    
    
    ### Problem 4 - B ###
    p4_b()
    
    
    ### Problem 4 - C ###
    p4_c()