import math

class MultinomialNB:
    def __init__(self, doc2words, documents, gtopics, alpha = 1.0):
        # document[id] = {'title': title, 'body': body, 'topic': topic, 'lewissplit': lewissplit}
        # doc2words[doc] = {word1: 1, word2: 3, ...}  (frequency map)
        self.documents = documents
        self.doc2words = doc2words
        self.gtopics = gtopics 
        self.alpha = alpha
    
        self.priors = None
        self.conditionals = None
        self.topics = None
        self.vocabulary = None

        self.is_fitted = False
        self.predictions = {}
    
    # can be used to find either total number of words or frequency of a particular word in a doc
    def _count(self, docID, word = None):
        if(word is None): return sum(self.doc2words[docID].values()) # sum of frequencies: total number of words
        else: return self.doc2words[docID][word]                     # return the frequency of word in doc
        
    # calculate the probability of word given topic: P(w | t)
    def _conditional(self, word, topic, word2topic, topic2freq):
        # p(w | t) = (number of occurrences of w in topic t + alpha) / (number of words in that topic + (# of words in total * alpha))
        
        nominator = word2topic[word].get(topic, 0) + self.alpha
        denominator = topic2freq[topic] + len(self.vocabulary) * self.alpha
        return nominator / denominator

    def _prior(self, topics, dataset):
        priors = {}
        for t in topics:
            priors[t] = float(len(topics[t])) / len(dataset)
        
        return priors
    
    def train(self, dataset):
        """
        We need:
            * vocabulary (set of unique words)

        To calculate the prior, we need:
            * Number of documents per topic

        To calculate the conditional, we need:
            * Number of occurrences of a specific word in a topic
            * Number of occurrences of that word for all topics
        """
        self.vocabulary = set()
        topics = {}
        word2topic = {}
        topic2freq = {} # topic2freq[t1] = number of words in that topic

        # dataset = list of (doc) pairs
        for doc in dataset:
            ts = self.documents[doc]['topics']
            ts = [t for t in ts if t in self.gtopics]

            for t in ts: topic2freq[t] = topic2freq.get(t, 0) + len(self.doc2words[doc].keys())

            for word in self.doc2words[doc].keys():
                self.vocabulary.add(word)
                if word not in word2topic: word2topic[word] = {}
                for t in ts: word2topic[word][t] = word2topic[word].get(t, 0) + 1

            for t in ts:
                if(t not in topics): topics[t] = []
                topics[t].append(doc)
        
        priors = self._prior(topics, dataset)

        # word2topic = {w1: {t1: 4, t2: 3, ...}, w2: {...}, ...}
        # vocabulary = {w1, w2, w3, ...}
        # topics = {t1: [doc1, ...], t2: [doc4, ...], ...}
        # priors = {t1: p(t1), t2: p(t2), ...}
        # topic2freq = {t1: # of words in t1, t2: # words in t2, ...}
        ############################################################

        # conditionals[w][t] = probability of word w given topic t 
        conditionals = {}
        for word in self.vocabulary:
            conditionals[word] = {}
            for topic in topics:
                conditionals[word][topic] = self._conditional(word, topic, word2topic, topic2freq)

        self.priors = priors
        self.conditionals = conditionals
        self.topics = topics
        self.is_fitted = True

    def predict(self, doc):
        # doc: document ID
        assert self.is_fitted

        scores = {}
        for topic in self.topics:
            scores[topic] = math.log(self.priors[topic])

            for word in self.doc2words[doc].keys():
                # TODO: What happens if word is not present in the vocabulary created by training set?
                # One alternative is to ignore the missing word, as it may not be relevant to the classification task.
                freq = self.doc2words[doc][word]
                if(word in self.vocabulary): scores[topic] += math.log(self.conditionals[word][topic]) * freq

        self.predictions[doc] = max(scores, key=scores.get) # return the most likely document
        return self.predictions[doc] # return the most likely document