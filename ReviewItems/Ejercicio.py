# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:28:35 2018

@author: Alan
"""

import nltk
import pickle
import re
import json
import operator
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader

def getCorpusTokens(NameDoc, encode):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
    try:
        f=open(NameDoc, encoding=encode)
        t=f.read()
        f.close()
    except Exception as e:
        return []
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tS = tS.replace('\x97', ' ')
    tS = tS.lower()
    tokens =  nltk.Text(nltk.word_tokenize(tS))
    return tokens

def getCorpusSentences(NameDoc, encode):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
    try:
        f=open(NameDoc, encoding=encode)
        t=f.read()
        f.close()
    except Exception as e:
        return []
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tS = tS.replace('\x97', ' ')
    tS = tS.lower()
    tokens =  nltk.Text(nltk.sent_tokenize(tS))
    return tokens

def cleanTokens(vocabulario):
    '''Solo limpia el vocabulario, usa una expresion regular para validar letra
    por letra y evitar que se ingresen caracteres no deseados o deconocidos en el corpus'''
    palabra_limpia = "";
    Arr = []
    for word in vocabulario:
        palabra_limpia = ""
        for letter in word:
            if re.match(r'[a-záéíóúñ]', letter):
                palabra_limpia += letter
        if palabra_limpia != "" and "www" not in palabra_limpia and "http" not in palabra_limpia:
            Arr.append(palabra_limpia)
    return Arr

def deleteStopWords(vocabulario, sw):
    new_v = []
    for word in vocabulario:
        if word not in sw:
            new_v.append(word)            
    return new_v

def loadLemmaDict():
    file = open('dictionary', 'rb')
    dictionary = pickle.load(file)
    file.close()
    return dictionary

def getAllReviews():
    TemporalName1 = ""
    TemporalName2 = ""
    Temporaltext = []
    texts = {}
    for i in range(0,6): #0, 6
        for j in range (0, 30):  #0, 30
            TemporalName1 = "moviles/no_" + str(i) + "_" + str(j) + ".txt"
            TemporalName2 = "moviles/yes_" + str(i) + "_" + str(j) + ".txt"
            #Temporaltext = getCorpusTokens(TemporalName1, 'utf-8')
            Temporaltext = getCorpusSentences(TemporalName1, 'utf-8')
            if len(Temporaltext) > 0:
                texts[TemporalName1[8:]] = Temporaltext
                
            #Temporaltext = getCorpusTokens(TemporalName2, 'utf-8')
            Temporaltext = getCorpusSentences(TemporalName2, 'utf-8') 
            if len(Temporaltext) > 0:
                texts[TemporalName2[8:]] = Temporaltext
    return texts

def lemmatizado(text, lemmas):
    new_text = []
    for word in text:
        dictLetter = lemmas[word[0]]
        for key in dictLetter:
            for Terminacion in dictLetter[key]['Terminaciones']:
                combinacion = key + "" + Terminacion
                if combinacion == word:
                    new_text.append({'Palabra':dictLetter[key]['Palabra'],
                                     'tipo': dictLetter[key]['Classificiacion']})
                    break
        new_text.append({'Palabra': word,
                         'tipo': "sn"})
    return new_text

def countNouns(texts):
    dictCount = {}
    for key in texts:
        for element in texts[key]:
            print(element)
            if element['tipo'].startswith("nc"):
                if element['Palabra'] in dictCount:
                    dictCount[ element['Palabra'] ] += 1
                else:
                    dictCount[ element['Palabra'] ] = 1

    return(dictCount)

def compute_ngrams(sequence, n):
    return zip(*[ sequence[index:] for index in range(n)])

def getTopNgrams(corpus, ngram_val = 2, limit = 5):
    tokens = corpus
    ngrams = compute_ngrams(tokens, ngram_val)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(), key =operator.itemgetter(1), reverse = True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams = [(' '.join(text), freq) for text, freq in sorted_ngrams]
    return sorted_ngrams

def getSentimentalDictionary():
    dict1 = {}
    doc = open('fullStrengthLexicon.txt', encoding='utf-8')
    contents = doc.read()
    contents = contents.split("\n")
    for line in contents:
        pala=line.split("\t")
        dict1[pala[0]] = pala[len(pala)-1] 
    return dict1

def word_in_sentence(text, SearchWord, sendDict):
    Sentences_with_word = []
    for sentence in text:
        if SearchWord in sentence:
            Sentences_with_word.append(sentence)

    for sentence in Sentences_with_word:
        for word in sentence:



    
sentimental_dict = getSentimentalDictionary()
textoSW = getCorpusTokens('stopwords_es.txt', 'utf-8') 
textoReviews = getAllReviews()
lemmas = loadLemmaDict()
for key in textoReviews:
    word_in_sentence(textoReviews[key])


