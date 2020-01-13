import nltk
import gensim
import string
import numpy
from nltk.corpus import treebank
from nltk.corpus import stopwords
from numpy import array

class Classifier:
    
    def __init__(*args, **kwargs):
        pass

    def similar(self, _input):
        return 0

# class JaccardSimilarityClassifer(Classifier):

#     def __init__(self, compareList, *args, **kwargs):
#         self.compareList = compareList

#     def similar(self, _input):
#         return max([jaccardSimilarity(_input, compareItem) for compareItem in self.compareList])

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
        print("loading ", category)
        path = "./keyword/" + category + ".txt"
        try:
            with open(path, "r") as f:
                keywords = f.read().split('\n')
                self.keywords = keywords
                self.wordVector = array([model[keyword] for keyword in keywords]).mean(axis=0)
        except Exception as e:
            print(e)

    def similar(self, _input):
        if (self.model == None):
            return 0
        
        stop_words = stopwords.words('english')
        words = nltk.pos_tag(nltk.word_tokenize(_input.lower()))
        words = [(word, pos) for word, pos in words if (word not in stop_words and word not in string.punctuation)]
        approximates = [ cossim(self.wordVector, self.model[word]) for word, pos in words if word in self.model] or [0]
        exacts = [0.5 if pos[0:2]=="VB" else 1 for word, pos in words if word in self.keywords] or [0]
        return max(approximates + exacts)
    
def main():
    nltk.data.path += ["./nltk_data"]
    categorys = [("restaurant"), ("shop"), ("facility")]
    
    print("loading word2vec")
    word2vec = gensim.models.KeyedVectors.load_word2vec_format("./nltk_data/models/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin", binary=True)
    

    classifiers = [KeyWordClassifer(category, model=word2vec) for category in categorys]

    
    while True:
        _input = input("input a string >")
        if (_input == ""):
            break
        similaritys = [(c.similar(_input), c.category) for c in classifiers] 
        print(similaritys)

if __name__ == "__main__":
    main()


