# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:28:35 2018

@author: Alan
"""

import nltk
import pickle
import re
import json
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader

def getCorpus(NameDoc, encode):
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
            Temporaltext = getCorpus(TemporalName1, 'latin-1')
            if len(Temporaltext) > 0:
                texts[TemporalName1[8:]] = Temporaltext
                
            Temporaltext = getCorpus(TemporalName2, 'utf-8') 
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


textoSW = getCorpus('stopwords_es.txt', 'utf-8') 
textoReviews = getAllReviews()
lemmas = loadLemmaDict()
dictionaryCount = {}
file = open('Res1.txt','w')
for key in textoReviews:
    print(key)
    textoReviews[key] = cleanTokens(textoReviews[key])
    textoReviews[key] = deleteStopWords(textoReviews[key], textoSW)
    textoReviews[key] = lemmatizado(textoReviews[key], lemmas)
    file.write(key)
    file.write("-------------\n") 
    file.write(json.dumps(textoReviews[key]))
    file.write("-------------\n\n\n") 

last = countNouns(textoReviews)
file.write("------------------------conteos----------------------------")
file.write(json.dumps(last))
file.close()































