import math

"""
When classifying a test document, the Bernoulli model
uses binary occurrence information, ignoring the number of occurrences,
whereas the multinomial model keeps track of multiple occurrences. As a
result, the Bernoulli model typically makes many mistakes when classifying
long documents. For example, it may assign an entire book to the class China
because of a single occurrence of the term China.
"""
class BernoulliNB:
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
    def _conditional(self, word, topic, word2topic, topics):
        # p(w | t) = (number of documents that have w in topic t + alpha) / (number of documents in topic + (2 * alpha))
        
        nominator = word2topic[word].get(topic, 0) + self.alpha
        denominator = len(topics[topic]) + 2.0 * self.alpha
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
            * Number of documents per topic
            * Number of documents that have word w in topic t
        """
        vocabulary = set()
        topics = {}
        word2topic = {}

        # dataset = list of (doc) pairs
        for doc in dataset:
            ts = self.documents[doc]['topics']
            ts = [t for t in ts if t in self.gtopics]

            for word in self.doc2words[doc].keys():
                vocabulary.add(word)

                if word not in word2topic: word2topic[word] = {}
                for t in ts: word2topic[word][t] = word2topic[word].get(t, 0) + 1

            for t in ts:
                if(t not in topics): topics[t] = []
                topics[t].append(doc)
        
        priors = self._prior(topics, dataset)

        # TODO: DIFFERENT FROM MULTINOMIAL --> word2topic[w1][t1]: documents that have w1 in topic t1 (regardless of the frequency)
        # word2topic = {w1: {t1: {doc1, doc3}, t2: {doc5, ...}, ...}, w2: {...}, ...} 
        
        ############################################################
        # vocabulary = {w1, w2, w3, ...}
        # topics = {t1: [doc1, ...], t2: [doc4, ...], ...}
        # priors = {t1: p(t1), t2: p(t2), ...}
        ############################################################

        # conditionals[w][t] = probability of word w given topic t 
        conditionals = {}
        for word in vocabulary:
            conditionals[word] = {}
            for topic in topics:
                conditionals[word][topic] = self._conditional(word, topic, word2topic, topics)

        self.vocabulary = vocabulary
        self.priors = priors
        self.conditionals = conditionals
        self.topics = topics
        self.is_fitted = True

    def predict(self, doc):
        """
        Important distinction: token and term
        token: not unique therefore reflects the frequency
        term: unique (used for bernoulli)
        """
        # doc: document ID
        assert self.is_fitted
        doc_vocab = set(self.doc2words[doc].keys())

        scores = {}
        for topic in self.topics:
            scores[topic] = math.log(self.priors[topic])
            for word in self.vocabulary:
                if(word in doc_vocab): scores[topic] += math.log(self.conditionals[word][topic]) 
                else: scores[topic] += math.log(1 - self.conditionals[word][topic])
        
        self.predictions[doc] = max(scores, key=scores.get) # return the most likely document
        return self.predictions[doc] # return the most likely document

