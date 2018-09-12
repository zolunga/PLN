#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 15:11:45 2018

@author: alan
"""

import nltk
import math
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import re
import operator
from decimal import Decimal

def getCorpus(NameDoc, encode):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
    f=open(NameDoc, encoding=encode)
    t=f.read()
    f.close()
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tS = tS.replace('\x97', ' ')
    tS = tS.replace('-', ' ')
    tS = tS.replace('¿', ' ')
    tS = tS.replace('?', ' ')
    tS = tS.replace('!', ' ')
    tS = tS.replace('¡', ' ')
    tS = tS.lower()
    tokens =  nltk.Text(nltk.word_tokenize(tS))
    return tokens

def deleteStopWords(vocabulario,sw):
    new_v = []
    for word in vocabulario:
        if word not in sw:
            new_v.append(word)            
    return new_v

def cleanTokens3(vocabulario):
    '''Solo limpia el vocabulario, usa una expresion regular para validar letra
    por letra y evitar que se ingresen caracteres no deseados o deconocidos en el corpus'''
    vl = []#voc limp
    palabra_limpia = "";
    for word in vocabulario:
        palabra_limpia = ""
        for letter in word:
            if re.match(r'[a-záéíóúñ]', letter):
                palabra_limpia += letter
        if palabra_limpia != "" and "www" not in palabra_limpia and "http" not in palabra_limpia:
            vl.append(palabra_limpia)
    #print(vl)
    return vl

def producto_punto(v1, v2):
    res = 0
    for i in range(0, len(v1)):
        res += (v1[i]*v2[i])
    return res

def Modulo(vector):
    sizeV = 0
    for element in vector:
        sizeV += math.pow(element,2)
    return math.sqrt(sizeV)


textoSW = getCorpus('stopwords_es.txt', 'utf-8') 
stopwords = cleanTokens3(textoSW)

texto = getCorpus('lemma.txt', 'latin-1')
vocabulario = []
for word in texto:
    if word != ',':
        vocabulario.append(word)
vocabulario = deleteStopWords(vocabulario, stopwords)        
print(len(set(vocabulario)))
