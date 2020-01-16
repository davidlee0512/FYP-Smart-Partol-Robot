import nltk
import gensim
import string
import numpy
from nltk.corpus import treebank
from nltk.corpus import stopwords
from numpy import array
import re
import MySQLdb

class Classifier:
    
    def __init__(*args, **kwargs):
        pass

    def similar(self, sentance):
        return 0

# class JaccardSimilarityClassifer(Classifier):

#     def __init__(self, compareList, *args, **kwargs):
#         self.compareList = compareList

#     def similar(self, sentance):
#         return max([jaccardSimilarity(sentance, compareItem) for compareItem in self.compareList])

#     def jaccardSimilarity (a, b):
#     seta = set(a)
#     setb = set(b)
#     return len(seta.intersection(setb))/len(seta.union(setb))

def cossim( vec1, vec2):
    return numpy.dot(gensim.matutils.unitvec(vec1), gensim.matutils.unitvec(vec2))

class KeyWordClassifer(Classifier):

    def __init__(self, category, *args, model=None, **kwargs):
        self.category = category
        self.model = model
        self.tags = []
        print("loading ", category)
        path = "./keyword/" + category + ".txt"
        try:
            with open(path, "r") as f:
                keywords = f.read().split('\n')
                self.keywords = keywords
                self.wordVector = array([model[keyword] for keyword in keywords]).mean(axis=0)
        except Exception as e:
            print(e)

    def similar(self, sentance):
        if (self.model == None):
            return 0
        
        stop_words = stopwords.words('english')
        words = nltk.pos_tag(nltk.word_tokenize(sentance.lower()))
        words = [(word, pos) for word, pos in words if (word not in stop_words and word not in string.punctuation)]
        approximates = [ cossim(self.wordVector, self.model[word]) for word, pos in words if word in self.model] or [0]
        exacts = [0.5 if pos[0:2]=="VB" else 1 for word, pos in words if word in self.keywords] or [0]
        return max(approximates + exacts)

    def getTagFromSentance(self, sentance):
        return [(max([self.model.similarity(word, tag) for word in nltk.word_tokenize(sentance.lower())]), tag)for tag in self.tags]


def getLocation(sentance):
    locationPatterns = [(r'([a-z]+) floor', "floor"), (r'terminal ([a-z]+)', "terminal"), (r'area ([a-z]+)', "area")]
    numberMaping = {"zero":0, "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, 
        "first":1, "second":2, "thrid":3, "fourth":4, "fifth":5, "sixth":6, "seventh":7, "eighth":8, "ninth":9}
    results = []
    for locationPattern,locationType in locationPatterns:
        result = re.search(locationPattern, sentance, re.IGNORECASE)
        if result and result.group(1) in numberMaping:
            results.append((numberMaping[result.group(1)], locationType))

    return results


def main():
    nltk.data.path += ["./nltk_data"]
    categorys = [("restaurant"), ("shop"), ("facility")]
    
    print("loading word2vec")
    word2vec = gensim.models.KeyedVectors.load_word2vec_format("./nltk_data/models/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin", binary=True)
    

    classifiers = {category: KeyWordClassifer(category, model=word2vec) for category in categorys}

    
    while True:
        sentance = input("input a string >")
        if (sentance == ""):
            break
        similarities = [(classifier.similar(sentance), category) for category, classifier in classifiers.items()] 
        print(similaritys)
        _, maxCategory = max(similarities)
        print("category: " + maxCategory)
        print("tag: " + classifiers[maxCategory].getTagFromSentance(sentance))

if __name__ == "__main__":
    main()


