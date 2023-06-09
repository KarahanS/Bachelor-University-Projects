from dataprocessor import DataProcessor
from splitter import Splitter
from models.multinomial import MultinomialNB
from models.bernoulli import BernoulliNB
from utils import *

import argparse
import time

def test(m, training, validation, test, gtopics, doc2word, documents, alpha):
    models = {'m': MultinomialNB, 'b': BernoulliNB}

    if(m == 'm'): print("Multinomial Naive Bayes")
    elif(m == 'b'): print("Bernoulli Naive Bayes")
    else: raise ValueError("Model should be either 'm' (Multinomial) or 'b' (Bernoulli)")

    start_time = time.time()
    print(">>> Testing with the given alpha value on test set. Both training and development tests are used for training.")
    nb = models[m](doc2word, documents, gtopics, alpha)
    nb.train(training | validation)
    predictions = predict(nb, test)
    correct, out, microf1, macrof1, microprecision, macroprecision, microrecall, macrorecall = evaluate(nb, test, gtopics, predictions)
    
    print("-"*50)
    print("Correct predictions: {}".format(correct), "out of: {}".format(out))
    print(" -- micro-precision: {}".format(round(microprecision, 3)), " -- macro-precision: {}".format(round(macroprecision, 3)))
    print(" -- micro-recall: {}".format(round(microrecall, 3)), " -- macro-recall: {}".format(round(macrorecall, 3)))
    print(" -- micro-f1: {}".format(round(microf1, 3)), " -- macro-f1: {}".format(round(macrof1, 3)))
    print(">>> Testing is completed. Elapsed time:", round(time.time() - start_time, 3), "seconds")

def main(input, splits, model, alpha):
    dataprocessor = load(input)
    data = load(splits)

    print("<-------------------------------------->")
    test(model, data.training, data.validation, data.test, data.gtopics, dataprocessor.doc2word, dataprocessor.documents, alpha)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # enter the relative path of your data folder from command line
    parser.add_argument("-i", "--input", help="Input vocabulary file (pickle) (output of dataprocessor)", default = "dataset.pkl") 
    parser.add_argument("-s", "--splits", help="Training, validation and test splits (pickle).", default="splits.pkl")
    parser.add_argument("-a", "--alpha", help="Alpha value for Laplace Smoothing", default=1.0, type=float)
    parser.add_argument("-m", "--model", help="Selection of Naive Bayes model: (m) for multinomial and (b) for bernoulli naive bayes.", required=True, choices=['m', 'b'])
    args = parser.parse_args()

    main(args.input, args.splits, args.model, args.alpha)