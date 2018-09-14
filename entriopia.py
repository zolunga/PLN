# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 20:41:31 2018

@author: Alan
"""
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


def getContext(vocabulario, palabra):
    '''
    Recibe el bocabulario completo y la palabra que va a buscar, retorna una lista
    de listas con el contexto del elemento en el texto
    '''
    ran = 4
    Contexs = []
    temp = []
    for x in range(0, len(vocabulario)):
        if vocabulario[x] == palabra:            
            for i in range((x - ran), (x + ran) ):
                if i > 0 and i <len(vocabulario):
                    if vocabulario[i] != palabra :
                        temp.append(vocabulario[i])
            #Contexs.append(temp)
            #temp = []
    #print("Lista de contexto de ", palabra, "Coincidencias:", cont)
    #print(Contexs)
    return temp

def Similarity_V(DictionaryV, word):
    Dictionary_sim = {}
    VectorWord = DictionaryV[word]
    VectorWord = np.array(VectorWord)
    VectorWordMod = (VectorWord**2)
    VectorWordMod = math.sqrt(VectorWordMod.sum())
    print(VectorWordMod)
    
    for key in DictionaryV:
        v = np.array(DictionaryV[key])
        vMod = v**2
        vMod = math.sqrt(v.sum())
        prod = vMod * vMod
        Dictionary_sim[key] = np.arccos(np.dot(VectorWord, v)/prod)
    return Dictionary_sim

def conPalabra(vocabulario):
    diccionario = {}
    total = len(vocabulario)
    for word in set(vocabulario):
        diccionario[word] = [0,0,0] #1 cantiddad, 2 probabilidad, 3 1 - prob
    for word in vocabulario:
        diccionario[word][0] += 1
    for word in diccionario:
        diccionario[word][1] = diccionario[word][0] / total 
        diccionario[word][2] = 1 - diccionario[word][1] 
    
    #sorted_d = sorted(diccionario.items(), key=operator.itemgetter(1))
    return diccionario


Texto = getCorpus("lemma.txt","latin-1")
Context_dictionary = {}
Vector_dictionary = {}
Prob_dictionary = {}
print("Diccionario de probabilidades")
Prob_dictionary = conPalabra(Texto)
print(Prob_dictionary)

'''
print("Iniciando Diccionario de contextos--", len(set(Texto)) )
for word in set(Texto):
    Context_dictionary[word] = getContext(Texto, word)
print("Iniciando Diccionario de vectores--")
for key in Context_dictionary:
    WordsContext = Context_dictionary[key]
    vector = []
    for word in Texto:
        vector.append(WordsContext.count(word))
    Vector_dictionary[key] = vector
    print(key)
    
print("Iniciando Calculo de similitud")
vector = Similarity_V(Vector_dictionary, "empresa")
print(vector)
'''

