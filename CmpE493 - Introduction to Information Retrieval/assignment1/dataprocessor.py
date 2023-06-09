import argparse
import glob
import re
import time
from tokenizer import Tokenizer, Stemmer
from trie import Trie
import html
import pickle

# regex constants
REUTERS = r'<REUTERS.*?REUTERS>'
NEWID = r'NEWID="(\d+)"'
TITLE = r'<TITLE>(.*?)</TITLE>'
BODY = r'<BODY>(.*?)</BODY>'
# observation: There is no news text with BODY but without TITLE. But there are texts with TITLE but without BODY.

class DataProcessor():
   def __init__(self, dataset, tokenizer: Tokenizer, dump = None):
      self.dataset = dataset
      self.tokenizer = tokenizer
      self.documents = {}
      self.corpus = {}
      self.stemmed_corpus = {} 
      self.vocabulary = Trie() 
      self.dumpfile = 'vocab.pickle'
   
   def parse(self):
      total = 0
      titleless = 0
      bodyless = 0

      self.path = dataset + "/*.sgm"
      for file in glob.glob(self.path):
         with open(file, 'r', encoding="latin-1") as f:
            text = f.read()
            _total, _titleless, _bodyless = self._parse(text)  
            total += _total
            titleless += _titleless
            bodyless += _bodyless

      print("Number of news texts without titles:", titleless)
      print("Number of news texts without body:", bodyless)

   def _parse(self, text):
      # parse the text to get NEWID, TITLE and BODY
      # firstly, get all REUTER news

      news = re.findall(REUTERS, text, flags=re.DOTALL)
      
      total = len(news)
      titleless = 0
      bodyless = 0

      for new in news:
         newid = int(re.search(NEWID, new).group(1))
         title = re.search(TITLE, new, flags=re.DOTALL)

         if(title is None): titleless += 1
         else: title = title.group(1)

         body = re.search(BODY, new, flags=re.DOTALL)

         if(body is None): bodyless += 1
         else: body = body.group(1)
         
         self.documents[newid] = {'title': title,'body': body}
      return total, titleless, bodyless

   # tokenize and create the vocabulary
   def tokenize(self):
      tokens = 0
      aftertokens = 0
      bag = set()
      for doc in self.documents: # keys
         title = self.documents[doc]['title']
         body = self.documents[doc]['body']

         def pipeline(text, startidx = 0):
            nonlocal tokens, aftertokens
            text = html.unescape(text)
            text = self.tokenizer.remove_punctuation(text)
            text = self.tokenizer.remove_digits(text)
            text = self.tokenizer.split(text)
            tokens += len(text)
            bag.update(text)
            text = self.tokenizer.casefold(text)
            aftertokens += len(text)
            for item in text: self.corpus[item] = self.corpus.get(item, 0) + 1 
            text = self.tokenizer.stem(text) 
            for item in text: self.stemmed_corpus[item] = self.stemmed_corpus.get(item, 0) + 1 
         
            # creating positional indexing
            for idx, word in enumerate(text): # words
               self.vocabulary.insert(word, docID = doc, position=idx + startidx)
            return text

         if(title is not None): title = pipeline(title)
         if(body is not None): body = pipeline(body, len(title))
      

      print("Processing: HTML Unescape --> Remove Punctuation --> Remove Digits --> Split --> Case Folding --> Stemming")
      print("Number of (total) tokens before casefolding:", tokens)
      print("Number of (total) tokens after casefolding:", aftertokens)
      print("Number of unique tokens before casefolding:", len(bag))
      print("Number of unique tokens after casefolding:", len(self.corpus))
      print("Number of unique tokens after stemming", len(self.stemmed_corpus))

      """
      a = sorted(self.corpus.items(), key=lambda item: item[1], reverse=True)[:100]
      b = sorted(self.stemmed_corpus.items(), key=lambda item: item[1], reverse=True)[:100]
      print("After case-folding (before stemming) \t\t\t  After stemming")
      for ax, bx in zip(a, b):
         axs = ax[0] + ": " + str(ax[1])
         bxs = bx[0] + ": " + str(bx[1])
         print(axs.ljust(50) + bxs)
      """

      
   def dump(self):
      # dump the vocabulary
      # open a file, where you ant to store the data
      with open(self.dumpfile, 'wb') as f:
         pickle.dump(self.vocabulary, f)



if __name__ == "__main__":
   parser = argparse.ArgumentParser()

   # enter the relative path of your data folder from command line
   parser.add_argument("-d", "--dataset", help="Dataset folder containing .sgm files", default = "dataset") 
   args = parser.parse_args()
   dataset = args.dataset

   tokenizer = Tokenizer(stemmer = Stemmer())
   dataprocessor = DataProcessor(dataset, tokenizer=tokenizer)
   print("> Reading the news dataset. Creating a dictionary of documents with TITLE and BODY components.")
   start_time = time.time()
   dataprocessor.parse()
   print("> News are read and a dictionary of documents is created. Elapsed time:", round(time.time() - start_time, 3), "seconds")

   start_time = time.time()
   print("> Proceeding with tokenization for news texts. Positional indexes will be prepared.")
   dataprocessor.tokenize()
   print("> Tokenization is completed. Positional indexes are generated. Elapsed time:", round(time.time() - start_time, 3), "seconds")

   start_time = time.time()
   print("> Positional indexes are being dumped with Pickle.")
   dataprocessor.dump()
   print("> Positional indexes are dumped at {}. Elapsed time:".format(dataprocessor.dumpfile), round(time.time() - start_time, 3), "seconds")