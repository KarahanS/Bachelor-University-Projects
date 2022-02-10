import numpy as np
import matplotlib.pyplot as plt 


def Gaussian(mean, variance, x):
    var = np.sqrt(variance) # deviation
    return 1/(var * np.sqrt(2*np.pi)) * (np.e ** (-1/2 * ((x - mean)/var) ** 2))

def KL_divergence(mean1, variance1, mean2, variance2):
    X = np.random.normal(0, 1, 1000)
    integral = 0
    for i in X:
        integral += np.log(Gaussian(mean1, variance1, i) / Gaussian(mean2, variance2, i))
    return integral / 1000

def binomial_gaussian_superimpose():
    nList = [5, 10, 20, 30, 40, 100]
    pList = [0.2, 0.33, 0.50]
    
    
    for n in nList:
        for p in pList:
            binomial = np.random.binomial(n, p, 10000)
            plt.hist(binomial,  bins = 150)
            
            axes = plt.gca()
            x_min, x_max = axes.get_xlim()
            
            x = np.arange(x_min,x_max,.01)
            f = 10000 * Gaussian(n*p, n*p*(1-p), x)
            
            plt.title("Histogram graphs for n={} p={}".format(n, p))
            plt.plot(x,f)
            plt.show()

def binomial_gaussian_side_by_side():
    nList = [5, 10, 20, 30, 40, 100]
    pList = [0.2, 0.33, 0.50]
    
    
    for n in nList:
        for p in pList:
            binomial = np.random.binomial(n, p, 10000)
            X = np.random.normal(n*p, n*p*(1-p), 10000)
            
            f, a = plt.subplots(1, 2)
            
            a[0].hist(binomial,  bins = 250)
            a[1].hist(X,  bins = 250)
            
            plt.setp(a[0], xlabel="Binomial Distribution".format(n, p))
            plt.setp(a[1], xlabel="Gaussian Distribution".format(n, p))
            plt.suptitle("Histogram graphs for n={} p={}".format(n, p))
            
            plt.show()

def plot_convolution(mean1, variance1, mean2, variance2):
    X = np.random.normal(mean1, variance1, 100000)
    Y = np.random.normal(mean2, variance2, 100000)

    plt.hist(X, bins = 500, range=[-5, 5])
    plt.xlabel("X")
    plt.ylabel("Frequency")
    plt.show()    
    
    plt.hist(Y, bins = 500, range=[-10, 15])
    plt.xlabel("Y")
    plt.ylabel("Frequency")
    plt.show()
    
    Z = X + Y
    plt.hist(Z, bins = 500, range=[-10, 15])
    plt.xlabel("Z = X + Y")
    plt.ylabel("Frequency")
    plt.show()


if __name__ == '__main__':
    
    ############## Question a ##############
    mean1 = -1      # X
    mean2 = 3       # Y
    variance1 = 1   # X
    variance2 = 4   # Y
    plot_convolution(mean1, variance1, mean2, variance2)
    #########################################
    
    
    ############## Question b ###############
    mean1 = 0
    mean2 = 0
    variance1 = 1
    variance2 = 4

    divergence = KL_divergence(mean1, variance1, mean2, variance2)
    print("Divergence = " + str(divergence))
    #########################################
    
    
    ############## Question c ##############
    binomial_gaussian_superimpose()
    binomial_gaussian_side_by_side()
    ########################################
