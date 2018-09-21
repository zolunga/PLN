import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import operator
import numpy as np
import math

def getCorpus(NameDoc, encode):
    ''' Obtiene los tokens del texto (considerando que ya esta limpio-lemma.py-)'''
    f=open(NameDoc, encoding=encode)
    t=f.read()
    f.close()
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tokens =  nltk.Text(nltk.word_tokenize(tS))
    return tokens


text = getCorpus('lemma.txt','latin-1')
textDD = nltk.DefaultTagger('NN')
patterns = [
    (r'.*ro$', 'ro'),
    (r'.*co$', 'co'),
    (r'.*no$', 'no'),
    (r'.*', 'Ninguno')
]
regexp = nltk.RegexpTagger(patterns)
#regexp.tag(textDD)
#print( textDD )
#print( regexp.tag(text) )



textTagger = nltk.pos_tag(text)
print(textTagger)

