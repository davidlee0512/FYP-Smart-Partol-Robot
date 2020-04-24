import nltk
import gensim
import string
import numpy
from nltk.corpus import treebank
from nltk.corpus import stopwords
from numpy import array
import re
import MySQLdb
import random
from googletrans import Translator

nltk.data.path += ["./nltk_data"]

class Classifier:
    
    def __init__(*args, **kwargs):
        pass

    def similar(self, sentence):
        return 0

# class JaccardSimilarityClassifer(Classifier):

#     def __init__(self, compareList, *args, **kwargs):
#         self.compareList = compareList

#     def similar(self, sentence):
#         return max([jaccardSimilarity(sentence, compareItem) for compareItem in self.compareList])

#     def jaccardSimilarity (a, b):
#     seta = set(a)
#     setb = set(b)
#     return len(seta.intersection(setb))/len(seta.union(setb))

def cossim(vec1, vec2):
    return numpy.dot(gensim.matutils.unitvec(vec1), gensim.matutils.unitvec(vec2))

#one Classifer per Category
class KeyWordClassifer(Classifier):

    def __init__(self, category, *args, model=None, tags=[], **kwargs):
        self.category = category
        self.model = model
        self.tags = [tag for tag in tags if tag in self.model]
        print("loaded tag: ", self.tags)
        print("loading ", category)
        path = "./chatbot/keyword/" + category + ".txt"
        try:
            with open(path, "r") as f:
                keywords = f.read().split('\n')
                self.keywords = keywords
                self.wordVector = array([model[keyword] for keyword in keywords]).mean(axis=0)
        except Exception as e:
            print(e)

    #return the probility of the sentence that belong this class
    def similar(self, sentence):
        if (self.model == None):
            return 0
        
        #geting stop word from NLTK
        stop_words = stopwords.words('english')

        #spilting words from sentence 
        words = nltk.pos_tag(nltk.word_tokenize(sentence.lower()))
        words = [(word, pos) for word, pos in words if (word not in stop_words and word not in string.punctuation)]

        #approximates the sentence by the overall wordVector
        approximates = [ cossim(self.wordVector, self.model[word]) for word, pos in words if word in self.model] or [0]

        #check if there is exact key word in the sentence
        exacts = [0.5 if pos[0:2]=="VB" else 1 for word, pos in words if word in self.keywords] or [0]

        return max(approximates + exacts)

    def getTagFromSentence(self, sentence):
        words = nltk.word_tokenize(sentence.lower())
        return [(max([self.model.similarity(word, tag) for word in words if word in self.model]), tag)for tag in self.tags]


def getLocation(sentence):
    #pattens for getting location
    locationPatterns = [(r'([a-z]+) floor', "{}/F"), (r'terminal ([a-z]+)', "terminal {0}")]
    numberMaping = {"zero":0, "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, 
        "first":1, "second":2, "thrid":3, "fourth":4, "fifth":5, "sixth":6, "seventh":7, "eighth":8, "ninth":9}
    
    results = []
    for locationPattern, locationFormat in locationPatterns:
        result = re.search(locationPattern, sentence, re.IGNORECASE)
        if result and result.group(1) in numberMaping:
            results.append(locationFormat.format(numberMaping[result.group(1)]))

    return results


class Chatbot():

    def __init__(self, categorys = ["restaurant", "shop", "facility"], dbargs = ("localhost", "root", "", "airport_info")):
        self.categorys = categorys
        self.db = MySQLdb.connect(*dbargs) or None

        print("loading word2vec")
        word2vecPath = "./nltk_data/models/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin"
        self.word2vec = gensim.models.KeyedVectors.load_word2vec_format(word2vecPath , binary=True)

        with self.db.cursor() as cursor:
            sql = "SELECT tag.name, category.name FROM tag INNER JOIN category ON tag.cid=category.id"
            cursor.execute(sql)
            result = cursor.fetchall()
            tags = {category: [tag for tag, _category in result if _category==category] for category in self.categorys}


        self.classifiers = {category: KeyWordClassifer(category, model=self.word2vec, tags=tags[category]) for category in self.categorys}
        
    def fetchInfoFromDB(self, category="", locations=[], tags=[]):
        if self.db and category:
            with self.db.cursor() as cursor:
                if tags:
                    sql = """
                        SELECT place.id, place.name, place.location 
                        FROM place, category, matching, tag 
                        WHERE category.name = '{0}' AND {1}tag.name IN {2} AND place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                        GROUP BY place.id 
                        HAVING COUNT(DISTINCT tag.name) = {3}
                        ORDER BY RAND()
                        LIMIT 1;
                        """.format(category, "".join(["place.location LIKE '%" + location + "%' AND " for location in locations]), "('"+ "', '".join(tags) +"')", len(tags))
                else:
                    sql = """
                        SELECT place.id, place.name, place.location 
                        FROM place, category, matching, tag 
                        WHERE category.name = '{0}' AND {1}place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                        GROUP BY place.id 
                        ORDER BY RAND()
                        LIMIT 1;
                        """.format(category, "".join(["place.location LIKE '%" + location + "%' AND " for location in locations]))

                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    return random.choice(result)
                else:
                    return None
                

    def askQuestion(self, question):
        """Ask a question to the chat bot
        
        Input
        question: the question you want to ask

        return the answer
        """

        translator = Translator()
        response =  translator.translate(question)
        questionLang = response.src
        question = response.text

        #get the probility of the question to each class
        similarities = [(classifier.similar(question), category) for category, classifier in self.classifiers.items()] 
        print(similarities)

        maxSimilarity, maxCategory = max(similarities)
        if (maxSimilarity < 0.5):
            return "I don't know your question, please ask again"

        #get the probility of each tag and get the location information in the question
        tagSimilarity = self.classifiers[maxCategory].getTagFromSentence(question)
        locationTags = getLocation(question)
        print("category: ", maxCategory)
        print("tag: ", tagSimilarity)
        print("locationTags: ", locationTags)

        #filter the tag with high similarity and use it to search the database
        tags = [tag for sim, tag in tagSimilarity if sim > 0.7]

        dbResult = self.fetchInfoFromDB(category=maxCategory, locations=locationTags, tags=tags)

        #TODO add output for chinese input
        if (questionLang == "zh-CN"):
            output = "搜尋結果:\n"
            output += "搜尋項目: " + maxCategory + "\n"

            if tags:
                output += "關鍵字: " + str(tags) + "\n"

            if locationTags:
                output += "地點: " + str(locationTags) + "\n"

            if dbResult:
                output += str(dbResult) 
            else:
                output += "找不到相關項目"
                return output

        output = "Here is the result:\n"
        output += "Category: " + maxCategory + "\n"

        if tags:
            output += "Tags: " + str(tags) + "\n"

        if locationTags:
            output += "Location: " + str(locationTags) + "\n"

        if dbResult:
            output += str(dbResult) 
        else:
            output += "Cannot find any result these requirement"
        

        return output

    def __del__(self):
        if self.db:
            self.db.close()


if __name__ == "__main__":
    chatbot = Chatbot()
    while True:
        sentence = input("input a string >")
        if (sentence == ""):
            break
        else:
            print(chatbot.askQuestion(sentence))



