import string
# stemmer: https://tartarus.org/martin/PorterStemmer/python.txt

class Stemmer():
    consonants = ['a', 'e', 'i', 'o', 'u']

    def __init__(self):
        self.b = ""
        self.k = 0
        self.k0 = 0
        self.j = 0 
        
    
    def cons(self, i):
        if self.b[i] in Stemmer.consonants:
            return 0
        if self.b[i] == 'y':
            if i == self.k0: return 1
            else: return (not self.cons(i - 1))
        return 1
    
    def m(self):
        n = 0
        i = self.k0
        while True:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while True:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i += 1
            i += 1

    def vowelinstem(self):
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0
    
    def doublec(self, j):
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j - 1]):
            return 0
        return self.cons(j)
    
    def cvc(self, i):
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i - 1) or not self.cons(i - 2):
            return 0
        ch = self.b[i]
        if ch in ['w', 'x', 'y']:
            return 0
        return 1
    
    def ends(self, s):
        length = len(s)

        if s[length - 1] != self.b[self.k]: return 0
        if length > (self.k - self.k0 + 1): return 0
        if self.b[self.k - length + 1: self.k + 1] != s: return 0

        self.j = self.k - length
        return 1
    
    def setto(self, s):
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length    

    def r(self, s):
        if self.m() > 0:
            self.setto(s)
    
    def step1ab(self):
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j 
            if self.ends("at"): self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch in ['l', 's', 'z']:
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i' + self.b[self.k + 1:]

    def step2(self):
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': 
            if self.ends("logi"):      self.r("log") # extra

    def step3(self):
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")   

    def step4(self):
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j
    
    def step5(self):
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1


    def stem(self, p, i, j):
        # p = word, i = starting index, j = end index
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b 

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]

class Tokenizer():
    def __init__(self, stemmer: Stemmer):
        self.stemmer = stemmer

    def remove_punctuation(self, text):
        return text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    
    def remove_digits(self, text):
        return text.translate(str.maketrans(string.digits, ' ' * len(string.digits)))

    def casefold(self, text: list[str]) -> list[str]:
        return [token.casefold() for token in text]
    
    def stem(self, wordlist: list[str]) -> list[str]:
        return [self.stemmer.stem(w, 0, len(w) - 1) for w in wordlist]
    
    def split(self, text, delimeter = None):
        return text.split(delimeter)
    

if __name__ == "__main__":
    stemmer = Stemmer()
    tokenizer = Tokenizer(stemmer = stemmer)
    print(tokenizer.remove_punctuation("Gfg, is best: for ! Geeks ;"))
    
    words = ["relational", "disgusting", "stemmer", "fertilizer", "whisperless"]
    for word in words:
        print(stemmer.stem(word, 0, len(word) - 1))

    s1 = "Stemming is funnier than a bummer says the sushi loving computer scientist"
    stemmed = []
    for w in s1.split(" "):
        stemmed.append(stemmer.stem(w, 0, len(w) - 1))
    print(" ".join(stemmed))

    print(tokenizer.casefold(["hey", "HERE"]))
    print(tokenizer.stemmer.stem("computer", 0, len("computer") - 1))
