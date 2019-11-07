import nltk
from nltk.corpus import treebank

#nltk.download('punkt')
nltk.data.path += ["./nltk_data"]

output = nltk.word_tokenize(input("input a string >"))
print(output)
output2 = nltk.pos_tag(output)
print(output2)
output3 = nltk.chunk.ne_chunk(output2)
print(output3)