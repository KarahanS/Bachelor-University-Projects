import argparse
from utils import *
from dataprocessor import DataProcessor

class Splitter:
    def __init__(self, training, validation, test, gtopics):
        self.training = training
        self.validation = validation
        self.test = test
        self.gtopics = gtopics

def main(input, ratio, num_topics, output):
    dataprocessor = load(input)
    
    print("Dataset is to be splitted into training, validation and test sets.")
    training, validation, test, gtopics = dataprocessor.create_dataset(num_topics, ratio)
    dataset = Splitter(training, validation, test, gtopics)
    dump(dataset, output)
    print("Splits are created and dumped into {}.".format(output))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # enter the relative path of your data folder from command line
    parser.add_argument("-i", "--input", help="Input vocabulary file (pickle) (output of dataprocessor)", default = "dataset.pkl") 
    parser.add_argument("-r", "--ratio", help="Training/validation split ratio", default=0.8, type=float)
    parser.add_argument("-n", "--num_topics", help="Number of topics to work on (defaults to 10)", default=10, type=int)
    parser.add_argument("-o", "--output", help="Output file for the splits (pickle)", default="splits.pkl")
    args = parser.parse_args()

    main(args.input, args.ratio, args.num_topics, args.output)