import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import operator
import numpy as np
import math
import re

def getCorpus(NameDoc, encode):
    ''' Obtiene los tokens del texto (considerando que ya esta limpio-lemma.py-)'''
    f=open(NameDoc, encoding=encode)
    t=f.read()
    f.close()
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tokens =  nltk.Text(nltk.word_tokenize(tS))
    return tokens

def getRawCorpus(NameDoc, encode):
    f = open(NameDoc, encoding=encode)
    t = f.read()
    f.close()
    t = t.replace('\x97', ' ')
    return t

def getArticles(TextE):
    ArticlesClean = []
    Articles = re.split(r'http://www.excelsior.com.mx/9604/960401/[\w]{3}[\d]{2}.html',TextE)
    print(len(Articles))
    for art in Articles:
        soup = BeautifulSoup(art, 'lxml')
        ArticlesClean.append(soup.get_text())
    return ArticlesClean

RawText = getRawCorpus('e960401.htm', 'latin-1')
ArticlesL = getArticles(RawText)
print(ArticlesL[4])







#---------------------------------------------------- CAP
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
#print(textTagger)
#----------------------------------------------------

