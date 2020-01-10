import nltk
import gensim
import string
from nltk.corpus import treebank
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

def jaccardSimilarity (a, b):
    seta = set(a)
    setb = set(b)
    return len(seta.intersection(setb))/len(seta.union(setb))


class Classifier:
    
    def __init__(self, compareList):
        self.compareList = compareList

    def similar(self, _input):
        similarList = [jaccardSimilarity(_input, compareItem) for compareItem in self.compareList]
        return max(similarList)
    


nltk.data.path += ["./nltk_data"]
questionCategory = [("restaurant_question.txt", "restaurant"), ("traffic_question.txt", "traffic")]
stop_words = stopwords.words('english')
classifiers = []

for path, category in questionCategory:
    try:
        print("loading ", category)
        sentences = open(path, "r").read().split('\n')
        sentences = [nltk.word_tokenize(s.lower()) for s in sentences if s]
        sentences = [ [word for word in s if (word not in stop_words and word not in string.punctuation)] for s in sentences]
        classifiers.append((Classifier(sentences), category))
    except Exception as e:
        print(e)


# print("loading word2vec")
# word2vec = gensim.models.KeyedVectors.load_word2vec_format("./nltk_data/models/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin", binary=True)

while True:
    _input = input("input a string >")
    if (_input == ""):
        break
    _input = nltk.word_tokenize(_input.lower())
    _input = [word for word in _input if (word not in stop_words and word not in string.punctuation)]
    similaritys = [(classifier.similar(_input), category) for classifier, category in classifiers] 
    print(similaritys)


