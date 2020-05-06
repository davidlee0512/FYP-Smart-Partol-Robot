import nltk
import gensim
import string
import numpy as np
from nltk.corpus import treebank
from nltk.corpus import stopwords
import re
import MySQLdb
import random
from googletrans import Translator
from nltk.parse.corenlp import CoreNLPDependencyParser
import os.path

nltk.data.path += [os.path.join(os.path.dirname(__file__),"./nltk_data")]

class Classifier:
    
    def __init__(self, *args, **kwargs):
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
    return np.dot(gensim.matutils.unitvec(vec1), gensim.matutils.unitvec(vec2))

#one Classifer per Category
class KeyWordClassifer(Classifier):

    def __init__(self, category, *args, model=None, tags=[], **kwargs):
        self.category = category
        self.model = model
        self.tags = [tag for tag in tags if tag in self.model]
        print("loaded tag: ", self.tags)
        print("loading ", category)
        path = os.path.join(os.path.dirname(__file__), "./keyword/" + category + ".txt")
        try:
            with open(path, "r") as f:
                keywords = f.read().split('\n')
                self.keywords = keywords
                self.wordVector = np.array([model[keyword] for keyword in keywords]).mean(axis=0)
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
        words = getWordList(sentence)

        return [(max([(self.model.similarity(word, tag), negSearch) for word, negSearch in words.values() if word in self.model]), tag)for tag in self.tags]

def getLocation(sentence): 
    words = getWordList(sentence)

    #pattens for getting location
    locationPatterns = {'floor': "{0}/F", 'terminal': "terminal {0}"}
    numberMaping = {"zero":0, "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, 
        "first":1, "second":2, "third":3, "fourth":4, "fifth":5, "sixth":6, "seventh":7, "eighth":8, "ninth":9}

    results = []
    for i, (word, isNeg) in words.items():
        if word in locationPatterns:
            gotNum = False
            number = None
            try:
                if words[i-1][0] in numberMaping:
                    number = numberMaping[words[i-1][0]]
                    gotNum = True
                elif words[i-1][0] in ["0","1","2","3","4","5","6","7","8","9"]:
                    number = int(words[i-1][0])
                    gotNum = True
            except:
                pass
            try:
                if words[i+1][0] in numberMaping:
                    number = numberMaping[words[i+1][0]]
                    gotNum = True
                elif words[i+1][0] in ["0","1","2","3","4","5","6","7","8","9"]:
                    number = int(words[i+1][0])
                    gotNum = True
            except:
                pass
            
            if gotNum:
                results.append((locationPatterns[word].format(number), isNeg))

    return results

def getWordList(sentence):
    notWords = ["not", "n't", "hate", "except", "without", "no"]

    #required the parser server to be open
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    #parse is a DependencyGraph object(nltk.parse.DependencyGraph)
    parse, = dep_parser.raw_parse(sentence.lower())

    words = {}

    #words is a list of (word, positive search or negative search)
    for node in parse.nodes.values():
        words[node["address"]] = (node["word"], False)

    #switching some part of the word into negative search if it is in notWords
    for node in parse.nodes.values():
        if node["word"] in notWords:
            def allDeps(_node):
                if _node:
                    i = _node["address"]
                    words[i] = (words[i][0], True)
                    for rel in _node["deps"]:
                        for j in _node["deps"][rel]:
                            allDeps(parse.nodes[j])


            def getObj(_node):
                base = _node
                try:
                    while "obj" not in base["deps"].keys():
                        base = parse.nodes[base["deps"]["xcomp"][0]]
                    base = parse.nodes[base["deps"]["obj"][0]]
                except:
                    base = None
                    
                return base

            def getObl(_node):
                base = _node
                try:
                    while "obl" not in base["deps"].keys():
                        base = parse.nodes[base["deps"]["xcomp"][0]]
                    base = parse.nodes[base["deps"]["obl"][0]]
                except:
                    base = None
                    
                return base
            
            #case a proposition
            if node["word"] in ["no", "without", "except"]:
                base = parse.nodes[node["head"]]
                allDeps(base)

            #case of not
            elif node["word"] in ["not", "n't"]:
                target = parse.nodes[node["head"]] if node["rel"] != "conj" else node
                if re.search(r"VB[a-zA-Z]*", target["tag"]):
                    allDeps(getObj(target))
                else:
                    allDeps(target)

                allDeps(getObl(target))

            #case of verb
            elif node["word"] in ["hate"]:
                allDeps(getObj(node))
                allDeps(getObl(node))


    return words

class Chatbot():

    def __init__(self, categorys = ["restaurant", "shop", "facility"], dbargs = ("localhost", "root", "", "airport_info")):
        self.categorys = categorys
        self.db = MySQLdb.connect(*dbargs) or None
        self.currentlocation = []
        self.currentTerminal = None
        print("loading word2vec")
        word2vecPath = os.path.join(os.path.dirname(__file__), "./nltk_data/models/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin")
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
                posTags = [tag for tag, isNeg in tags if not isNeg]
                negTags = [tag for tag, isNeg in tags if isNeg]

                posLocations = [location for location, isNeg in locations if not isNeg]
                negLocations = [location for location, isNeg in locations if isNeg]

                posLocationQuery = "".join(["place.location LIKE '%" + posLocation + "%' AND " for posLocation in posLocations])
                negLocationQuery = "".join(["place.location NOT LIKE '%" + negLocation + "%' AND " for negLocation in negLocations])

                if posTags and negTags:
                    print(0)
                    sql = f"""
                    SELECT * FROM place WHERE place.id IN (
                        SELECT place.id
                        FROM place, category, matching, tag 
                        WHERE category.name = '{category}' AND {posLocationQuery} {negLocationQuery} tag.name IN ('{"', '".join(posTags)}') AND place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                        GROUP BY place.id 
                        HAVING COUNT(DISTINCT tag.name) = {len(posTags)}
                    ) AND place.id NOT IN (
                        SELECT place.id
                        FROM place, category, matching, tag 
                        WHERE category.name = '{category}' AND tag.name IN ('{"', '".join(negTags)}') AND place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                        GROUP BY place.id
                    )
                    """
                elif negTags:
                    print(1)
                    sql = f"""
                        SELECT * FROM place WHERE place.id IN (
                            SELECT place.id
                            FROM place, category, matching, tag 
                            WHERE category.name = '{category}' AND {posLocationQuery} {negLocationQuery} place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                            GROUP BY place.id 
                        ) AND place.id NOT IN (
                            SELECT place.id
                            FROM place, category, matching, tag 
                            WHERE category.name = '{category}' AND tag.name IN ('{"', '".join(negTags)}') AND place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                            GROUP BY place.id
                        )
                        """
                elif posTags:
                    print(2)
                    sql = f"""
                        SELECT place.id, place.name, place.location 
                        FROM place, category, matching, tag 
                        WHERE category.name = '{category}' AND {posLocationQuery} {negLocationQuery} tag.name IN ('{"', '".join(posTags)}') AND place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                        GROUP BY place.id 
                        HAVING COUNT(DISTINCT tag.name) = {len(posTags)}
                        """
                else:
                    print(3)
                    sql = f"""
                        SELECT place.id, place.name, place.location 
                        FROM place, category, matching, tag 
                        WHERE category.name = '{category}' AND {posLocationQuery} {negLocationQuery} place.id = matching.pid AND tag.id = matching.tid AND category.id = tag.cid 
                        GROUP BY place.id
                        """

                print("sql: ", sql)

                cursor.execute(sql)
                result = cursor.fetchall()
                return result
                
    def renewlocation(self,locations):
        self.currentlocation = locations.copy()
        return None
    def checktermianl(self,locations):
        locationlist = locations.copy()
        for x in locationlist:
            if x[0] == "terminal 1" or x[0] =="terminal 2":
                self.currentTerminal=x
                locations.remove(x)
        return locations
    def resetall(self):
        self.currentlocation = []
        self.currentTerminal = None    

    def askQuestion(self, question):
        """Ask a question to the chat bot
        
        Input
        question: the question you want to ask

        return the answer
        """

        question = question.replace('\n', '')

        translator = Translator()
        questionLang = translator.detect(question).lang
        question = translator.translate(question, src="zh-CN").text
        print("questionLang: ", questionLang)
        print("question: ", question)

        #get the probility of the question to each class
        similarities = [(classifier.similar(question), category) for category, classifier in self.classifiers.items()] 
        print(similarities)

        maxSimilarity, maxCategory = max(similarities)
        if (maxSimilarity < 0.4):
            return "我不知道你的問題，請重新發問" if (questionLang == "zh-CN") else "I don't know your question, please ask again"

        #get the probility of each tag and get the location information in the question
        tagSimilarity = self.classifiers[maxCategory].getTagFromSentence(question)

        #try to get location tag in the question
        locationTags = getLocation(question)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #need to remove this line in later(in order to use the isNeg in location tag)
        #locationTags = [locationtag for locationtag, isNeg in locationTags]

        #use location in previous question as the lcoation on this
        if not locationTags:
            temp = self.currentlocation.copy()
            if self.currentTerminal != None:
                temp.append(self.currentTerminal)
            locationTags= temp
        else:
            locationTags=self.checktermianl(locationTags)
            print("current terminal:" , self.currentTerminal)
            #print("terminal: ", self.currentTerminal)
           # print("remove location : ", locationTags)
            self.renewlocation(locationTags)
            if self.currentTerminal != None:
                locationTags.append(self.currentTerminal)
            
        print("category: ", maxCategory)
        print("tag: ", tagSimilarity)
        print("locationTags: ", locationTags)

        #filter the tag with high similarity and use it to search the database
        tags = [(tag,isNeg) for (sim, isNeg), tag in tagSimilarity if sim > 0.7]
     
        dbResult = self.fetchInfoFromDB(category=maxCategory, locations=locationTags, tags=tags)

        output = ""
        if (questionLang == "zh-CN"):
            output += "搜尋結果:\n"
            output += "搜尋項目: " + maxCategory + "\n"

            if tags:
                output += "關鍵字: " + str(tags) + "\n"

            if locationTags:
                output += "地點: " + str(locationTags) + "\n"

            if dbResult:
                output += "\n".join((str(result) for result in dbResult))
            else:
                output += "找不到相關項目"
                return output
        else:
            output = "Here is the result:\n"
            output += "Category: " + maxCategory + "\n"

            if tags:
                output += "Tags: " + str(tags) + "\n"

            if locationTags:
                output += "Location: " + str(locationTags) + "\n"

            if dbResult:
                output += "\n".join((str(result) for result in dbResult))
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



