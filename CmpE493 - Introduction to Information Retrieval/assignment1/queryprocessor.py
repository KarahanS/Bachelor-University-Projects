import argparse
import pickle
import time
import sys
from tokenizer import Stemmer

# Query Processor
class QueryProcessor():
    def __init__(self, dumpfile = "vocab.pickle"):
        with open(dumpfile, 'rb') as f:
            self.vocabulary = pickle.load(f)
        self.stemmer = Stemmer()

    def exists(self, words):
        return all(self.vocabulary.search(word) is not False for word in words)
    
    def phrase_query(self, words):
        # "w1 w2 w3 ... wn"
        out = []

        # observe that: 
        words = [self.stemmer.stem(w, 0, len(w) - 1) for w in words]
        if(not self.exists(words)):
            print("Out-of-vocabulary words.", end = " ")
            return []
        
        indexes = [self.vocabulary.search(word).index for word in words]
        
        for docID in indexes[0]:
            if(all([docID in indexes[idx] for idx, _ in enumerate(words)])):
                # iterate
                postlists = [index[docID].second for index in indexes]
                wi = [0] * len(words)
                while(wi[0] < len(postlists[0])):
                    position1 = postlists[0][wi[0]]
                    fail = False
                    for idx in range(1, len(words)):
                        position = position1 + idx         # supposed-to-be position
                        if(wi[idx] >= len(postlists[idx])):
                            wi[0] = len(postlists[0]) # suicide
                            fail = True
                            break
                        elif(postlists[idx][wi[idx]] < position):
                            wi[idx] += 1
                            fail = True
                            break
                        elif(postlists[idx][wi[idx]] > position):
                            wi[0] += 1
                            fail = True
                            break
                    
                    if(not fail):
                        out.append(docID)
                        break
        return out
                        
    def proximity_query(self, w1:str, w2:str, k:int):
        out = []
        w1 = self.stemmer.stem(w1, 0, len(w1) - 1)
        w2 = self.stemmer.stem(w2, 0, len(w2) - 1)

        if(not self.exists([w1, w2])):
            print("Out-of-vocabulary words.", end=" ")
            return []
        
        w1_index = self.vocabulary.search(w1).index
        w2_index = self.vocabulary.search(w2).index
        # posting:  word, doc_frequency, index  (index is a dictionary: {docID: (first: # of occurrences, second: list)})
        for docID in w1_index:
            if(docID in w2_index):
                # iterate
                poslist1 = w1_index[docID].second
                poslist2 = w2_index[docID].second

                i, j = 0, 0
                while(i < len(poslist1) and j < len(poslist2)):
                    position1 = poslist1[i]
                    position2 = poslist2[j]
                    if(abs(position1 - position2) <= (k + 1)):
                        out.append(docID)
                        break
                    else:
                        if position1 > position2: j += 1
                        else: i += 1
        return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = sys.argv

    start_time = time.time()
    print("> Reading the positional indexes and creating a query processor.")
    processor = QueryProcessor()
    print("> Query processor is created. Elapsed time:", round(time.time() - start_time, 3), "seconds")


    if(len(args) <= 3): # candidate for phrase query
        words = args[1].split()
        out = processor.phrase_query(words)
        print("List of documents:", out)
    else:  # candidate for proximity query
        try:
            w1, k, w2 = args[1], int(args[2]), args[3]
            assert k >= 0
            out = processor.proximity_query(w1, w2, k)
            print("List of documents:", out)
        except:
            print("A problem occurred while parsing the proximity query. Please make sure that your query is valid. Keep in mind that the integer k must be non-negative.")

