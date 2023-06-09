from dataprocessor import DataProcessor
from splitter import Splitter
from models.multinomial import MultinomialNB
from models.bernoulli import BernoulliNB
from utils import *

import argparse
import time
import random

def ar_test(r, mnb_macrof1, bnb_macrof1, mnb, bnb, data):
    print(">>> Randomization test is started.")
    s = abs(mnb_macrof1 - bnb_macrof1)
    counter = 0

    mnb_base_predictions = mnb.predictions.copy()
    bnb_base_predictions = bnb.predictions.copy()

    start_time = time.time()
    for _ in range(r):
        mnb.predictions = mnb_base_predictions.copy()
        bnb.predictions = bnb_base_predictions.copy()

        for instance in data.test:
            mnb_prediction = mnb.predictions[instance]
            bnb_prediction = bnb.predictions[instance]

            # swap the predictions by %5 probability
            if(random.random() < 0.05):
                mnb.predictions[instance] = bnb_prediction
                bnb.predictions[instance] = mnb_prediction
            # calculate
        _, _, _, mnb_macrof1, _, _, _, _ = evaluate(mnb, data.test, data.gtopics, mnb.predictions)
        _, _, _, bnb_macrof1, _, _, _, _ = evaluate(bnb, data.test, data.gtopics, bnb.predictions)

        if(abs(mnb_macrof1 - bnb_macrof1) >= s):
            counter += 1
    p = (counter+1) / (r+1)
    print("Randomization test is completed. Elapsed time:", round(time.time() - start_time, 3), "seconds")
    print(">>> p-value:", round(p, 6))
    if(p < 0.05):
        print(">>> The difference between the two models is statistically significant.")
    else:
        print(">>> The difference between the two models is not statistically significant.")

def main(input, splits, malpha, balpha, r):
    dataprocessor = load(input)
    data = load(splits)
    
    # test the models with the given alpha value on training set
    mnb = MultinomialNB(dataprocessor.doc2word, dataprocessor.documents, data.gtopics, malpha)
    bnb = BernoulliNB(dataprocessor.doc2word, dataprocessor.documents, data.gtopics, balpha)

    mnb.train(data.training | data.validation)
    bnb.train(data.training | data.validation)

    start_time = time.time()
    print(">>> Predictions of Multinomial NB are calculated.")
    mnb_predictions = predict(mnb, data.test)
    _, _, _, mnb_macrof1, _, _, _, _ = evaluate(mnb, data.test, data.gtopics, mnb_predictions)
    print("Predictions of Multinomial NB are calculated. Elapsed time:", round(time.time() - start_time, 3), "seconds")
    print(">>> Predictions of Bernoulli NB are calculated.")
    bnb_predictions = predict(bnb, data.test)
    _, _, _, bnb_macrof1, _, _, _, _ = evaluate(bnb, data.test, data.gtopics, bnb_predictions)
    print("Predictions of Bernoulli NB are calculated. Elapsed time:", round(time.time() - start_time, 3), "seconds")

    ar_test(r, 
            mnb_macrof1,  
            bnb_macrof1, 
            mnb, 
            bnb,
            data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # enter the relative path of your data folder from command line
    parser.add_argument("-i", "--input", help="Input vocabulary file (pickle) (output of dataprocessor)", default = "dataset.pkl") 
    parser.add_argument("-s", "--splits", help="Training, validation and test splits (pickle).", default="splits.pkl")
    parser.add_argument("-ma", "--multinomial_alpha", help="Alpha value for Laplace Smoothing - Multinomial Distribution", default=1.0, type=float)
    parser.add_argument("-ba", "--bernoulli_alpha", help="Alpha value for Laplace Smoothing - Bernoulli Distribution", default=1.0, type=float)
    parser.add_argument("-r", "--randomization", help="Number of randomization tests.", default=1000, type=int)
    args = parser.parse_args()

    main(args.input, args.splits, args.multinomial_alpha, args.bernoulli_alpha, args.randomization)