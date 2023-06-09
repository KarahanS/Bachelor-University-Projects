from dataprocessor import DataProcessor
from splitter import Splitter
from models.multinomial import MultinomialNB
from models.bernoulli import BernoulliNB
from utils import *

import argparse
import time

def tune(m, training, validation, gtopics, doc2word, documents, alphas=[1.0]):
    models = {'m': MultinomialNB, 'b': BernoulliNB}

    if(m == 'm'): print("Multinomial Naive Bayes")
    elif(m == 'b'): print("Bernoulli Naive Bayes")
    else: raise ValueError("Model should be either 'm' (Multinomial) or 'b' (Bernoulli)")

    # training, validation, test: list of doc IDs
    """
    Source: https://datascience.stackexchange.com/a/24051
     In a multi-class classification setup, micro-average is preferable 
     if you suspect there might be class imbalance (i.e you may have many more examples of one class than of other classes).
    """

    
    print(">>> Training with the given alpha value(s) on training set. Evaluating the model on development set.")
    for alpha in alphas:
        start_time = time.time()
        nb = models[m](doc2word, documents, gtopics, alpha)
        nb.train(training)
        predictions = predict(nb, validation)
        correct, out, microf1, macrof1, microprecision, macroprecision, microrecall, macrorecall = evaluate(nb, validation, gtopics, predictions)
        print("-"*50)
        print("Alpha: {}".format(alpha))
        print("Correct predictions: {}".format(correct), "out of: {}".format(out))
        print(" -- micro-precision: {}".format(round(microprecision, 3)), " -- macro-precision: {}".format(round(macroprecision, 3)))
        print(" -- micro-recall: {}".format(round(microrecall, 3)), " -- macro-recall: {}".format(round(macrorecall, 3)))
        print(" -- micro-f1: {}".format(round(microf1, 3)), " -- macro-f1: {}".format(round(macrof1, 3)))
        print(">>> Evaluation is completed. Elapsed time:", round(time.time() - start_time, 3), "seconds")

def main(input, splits, model, alpha):
    dataprocessor = load(input)
    data = load(splits)
    
    print("<-------------------------------------->")
    tune(model, data.training, data.validation, data.gtopics, dataprocessor.doc2word, dataprocessor.documents, alpha)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # enter the relative path of your data folder from command line
    parser.add_argument("-i", "--input", help="Input vocabulary file (pickle) (output of dataprocessor)", default = "dataset.pkl") 
    parser.add_argument("-s", "--splits", help="Training, validation and test splits (pickle).", default="splits.pkl")
    parser.add_argument("-m", "--model", help="Selection of Naive Bayes model: (m) for multinomial and (b) for bernoulli naive bayes.", required=True, choices=['m', 'b'])
    parser.add_argument("-a", "--alphas", help="Alpha values for the model.", default=[1.0], nargs='+', type=float)
    args = parser.parse_args()

    main(args.input, args.splits, args.model, args.alphas)