import nltk

#nltk.download('punkt')
nltk.data.path += "\\nltk_data"

output = nltk.word_tokenize(input("input a string >"))
print(output)