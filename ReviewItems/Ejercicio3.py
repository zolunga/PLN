
import nltk
import pickle

def loadLemmaDict():
    file = open('dictionary', 'rb')
    dictionary = pickle.load(file)
    file.close()
    return dictionary

def id_process(doc):
	sentences = nltk.sent_tokenize(doc)
	sentences = [nltk.pos_tag(sent) for sent in sentences]

def pos_tag(text, dictionary):
    for word in text:
        temp_d = dictionary[word.starWith()]
        for raiz in temp_d:
            genWord = raiz + temp_d[raiz]['terminacion']

cadena = "Los estudiantes de ESCOM ganaron el premio Nobel."
sentence = nltk.pos_tag(nltk.word_tokenize(cadena))

grammar = "NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar)
result = cp.parse(sentence)
print(result)
result.draw()