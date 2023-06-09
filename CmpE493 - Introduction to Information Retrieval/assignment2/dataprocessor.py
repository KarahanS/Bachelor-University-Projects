import argparse
import glob
import re
import time
import html
import random

from tokenizer import Tokenizer, Stemmer
from utils import *

# regex constants
REUTERS = r'<REUTERS.*?REUTERS>'
HEADER = r'TOPICS="(.*?)".*?LEWISSPLIT="(.*?)".*?NEWID="(\d+)"'
TITLE = r'<TITLE>(.*?)</TITLE>'
TOPICS = r'<TOPICS>(.*?)</TOPICS>'
D = r'<D>(.*?)</D>'
BODY = r'<BODY>(.*?)</BODY>'

# observation: 
#   There is no news text with BODY but without TITLE. But there are texts with TITLE but without BODY.
#   LEWISSPLIT is present in all REUTERS texts.

# PROBLEM:
#   there are topics where TOPICS:YES but there is not really a topic (it's just "").
class DataProcessor():
    def __init__(self, dataset):
        self.dataset = dataset

        self.documents = {}  # document[id] = {'title': title, 'body': body, 'topics': [t1, t2, t3], 'lewissplit': lewissplit}
        self.topic2doc = {}  # topic2doc[topic] = [doc1, doc2, ...]
        self.doc2word = {}   # vocab[doc] = {word1: 1, word2: 3, ...}  (frequency map)
    
    def parse(self):
        total = 0
        titleless = 0
        bodyless = 0

        self.path = self.dataset + "/*.sgm"
        for file in glob.glob(self.path):
            with open(file, 'r', encoding="latin-1") as f:
                text = f.read()
                _total, _titleless, _bodyless = self._parse(text)  
                total += _total
                titleless += _titleless
                bodyless += _bodyless
    
        print("(Ignored) Number of news texts without titles:", titleless)
        print("(Ignored) Number of news texts without body:", bodyless)
        
    def _parse(self, text):
        # parse the text to get NEWID, TITLE and BODY
        # firstly, get all REUTER news
        news = re.findall(REUTERS, text, flags=re.DOTALL)
        
        total = len(news)
        titleless = 0
        bodyless = 0

        for new in news:
            header = re.search(HEADER, new)
            topic = header.group(1)
            lewissplit = header.group(2)
            newid = header.group(3)
            
            title = re.search(TITLE, new, flags=re.DOTALL)
            if(title is None): titleless += 1
            else: title = title.group(1)

            body = re.search(BODY, new, flags=re.DOTALL)
            if(body is None): bodyless += 1
            else: body = body.group(1)

            topics = None
            if(topic == 'YES' and title is not None and body is not None): 
                topic = re.search(TOPICS, new, flags=re.DOTALL).group(1)
                topics = re.findall(D, topic)
                # increment the frequency of the topic

                for topic in topics:
                    if topic in self.topic2doc: self.topic2doc[topic].append(newid)
                    else: self.topic2doc[topic] = [newid]

            if(title is not None and body is not None):
                self.documents[newid] = {'title': title,'body': body, 'topics': topics, 'lewissplit': lewissplit}
            
        return total, titleless, bodyless

    # tokenize and create the vocabulary
    def tokenize(self):
        unique = set()
        stemmer = Stemmer()

        for doc in self.documents: # keys
            title = self.documents[doc]['title']
            body = self.documents[doc]['body']
            self.doc2word[doc] = {}

            def pipeline(text):
                preprocessing_functions = [
                    html.unescape,
                    Tokenizer.remove_punctuation,
                    Tokenizer.remove_digits,
                    Tokenizer.split,
                    Tokenizer.casefold,
                    Tokenizer.remove_stopwords,
                    stemmer.stem
                ]
                # Apply functions
                for func in preprocessing_functions:
                    text = func(text)

                unique.update(text)
                
                # create frequency map
                freq = {}
                for word in set(text):
                    freq[word] = text.count(word)

                """
                >>> a = {'b': 1, 'c': 2}
                >>> a.update({'b':2, 'd':1})
                >>> a
                {'b': 2, 'c': 2, 'd': 1}
                """
                self.doc2word[doc].update(freq)
                return text

            if(title is not None): title = pipeline(title)
            if(body is not None): body = pipeline(body)

        print("Processing: HTML Unescape --> Remove Punctuation --> Remove Digits --> Split  --> Case Folding --> Remove Stopwords --> Stemming")
        print("Size of the resulting vocabulary:", len(unique))

    def create_dataset(self, ntopics = 10, ratio = 0.8):
        _sorted = dict(sorted(self.topic2doc.items(), key=lambda item: len(item[1]), reverse=True))
        topics = list(_sorted.keys())[:ntopics]
        
        print("Top 10 topics: ", topics)
        tcounter = {}   # tcounter[topic1] = [# training docs, # test docs]
        for t in topics: tcounter[t] = [0, 0]
        cnt = 0

        training = set()
        validation =set()
        test = set()
        train_vocab_set = set()
        test_vocab_set = set()
        not_used_set = set()
        not_used = set()
        for topic in topics:
            temp = []
            for doc in self.topic2doc[topic]:
                # doc belongs to the given topic
                lewissplit = self.documents[doc]['lewissplit']
                if(lewissplit == 'TRAIN'): 
                    temp.append(doc)
                    tcounter[topic][0] += 1
                    train_vocab_set.update(self.doc2word[doc].keys())
                elif(lewissplit == 'TEST'): 
                    test.add(doc)
                    tcounter[topic][1] += 1
                    test_vocab_set.update(self.doc2word[doc].keys())
                else: 
                    not_used_set.update(self.doc2word[doc].keys())
                    not_used.add(doc)
                    # lewissplit = 'NOT-USED'

            random.shuffle(temp)
            validation.update(temp[:int(len(temp) * (1 - ratio))])
            training.update(temp[int(len(temp) * (1 - ratio)):])

        for doc in training | validation | test:
            ts = self.documents[doc]['topics']
            inter = list(set(topics) & set(ts))
            if(len(inter) > 1): cnt+=1
        
        print("Vocab size for training set:", len(train_vocab_set))
        print("Vocab size for test + training set:", len(test_vocab_set | train_vocab_set))
        print("Vocab size for testset + training set + not-used:", len(test_vocab_set | train_vocab_set | not_used_set))
        print("Number of documents labeled with more than one of the top 10 classes: {}".format(cnt))
        for topic in topics:
            print("{}: \n".format(topic), 
                    "    training: {} \n".format(tcounter[topic][0]),
                    "    test: {}".format(tcounter[topic][1]))
        
        print("Total number of documents in training: {} (development: {})".format(len(training) + len(validation), len(validation)))
        print("Total number of documents in test: {}".format(len(test)))
        return training, validation, test, topics
    
def main(datafolder, output):
    dataprocessor = DataProcessor(datafolder)
    print(">>> Reading the news dataset. Creating a dictionary of documents with TITLE and BODY components.")
    start_time = time.time()
    dataprocessor.parse()
    print(">>> News are read and a dictionary of documents is created. Elapsed time:", round(time.time() - start_time, 3), "seconds")

    start_time = time.time()
    print(">>> Proceeding with tokenization for news texts.")
    dataprocessor.tokenize()
    print(">>> Tokenization is completed. Elapsed time:", round(time.time() - start_time, 3), "seconds")

    dump(dataprocessor, output)
    print(">>> Dataset is created and dumped into {}.".format(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # enter the relative path of your data folder from command line
    parser.add_argument("-d", "--datafolder", help="Dataset folder containing .sgm files", default = "dataset") 
    parser.add_argument("-o", "--output", help="Output file name", default = "dataset.pkl")
    args = parser.parse_args()

    main(args.datafolder, args.output)