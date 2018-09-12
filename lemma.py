# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import nltk
import math
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import re
import operator
from decimal import Decimal
import time


#f=open('e960401.htm', encoding='latin-1')
#t=f.read()
#f.close()
 
#soup = BeautifulSoup(t, 'lxml')
#tS = soup.get_text()
#tS = tS.replace('\x97', ' ')
#tokens =  word_tokenize(tS)
#tokens_nltk = nltk.Text(tokens)
#print("Cantidad de palabras del texto:",len(tokens_nltk))
#print("Palabras diferentes:",len(set(tokens)) )
#print("---------Palbaras similares---------")
#print(tokens_nltk.similar("empresa"))
#print("------------------------------------")
#temporal = tokens_nltk.similar("empresa")
#f=open('e960401.txt', 'w')
#f.write(tS)
#f.close()

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
  
def hasNumber(Str):
    ''' retorna true si encuentra un numero en la cadena '''
    return any(char.isdigit() for char in Str)

def cleanTokens3(vocabulario):
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
    print("cleanTokens terminado")
    return Arr

def Lemmas(vocabulario):
    print("------------------------------------------------------------------------------------------------------------------------lematizando")
    palabra_lemmatizada = ""
    listEscritura = []
    for word in vocabulario:
        palabra_lemmatizada = word
        dic_temporal = dic_lemmas[word[0]]
        for key in dic_temporal:
            if word.startswith(key):
                for i in range(0,len(dic_temporal[key])):
                    if(word == dic_temporal[key][0]):
                        palabra_lemmatizada = dic_temporal[key][0]
                        break
                    if dic_temporal[key][i] == "":
                        continue
                    stringtem = key + dic_temporal[key][i]
                    if(word == stringtem):
                        palabra_lemmatizada = dic_temporal[key][0]
                        break
        listEscritura.append(palabra_lemmatizada)
    file=open("lemma.txt", "w")
    file.write(" ".join(listEscritura))
    file.close()
            

file=open("generate.txt", encoding="latin-1")
temp=file.read()
file.close()

lin = temp.split("\n")
lin = lin[19:]
dic_lemmas = {}
for line in lin:
    lineSplit = line.split(" ")
    if len(lineSplit) > 1:
        lemma = lineSplit[0]
        x = lemma.find("#")
        #print(lemma[0])
        if lemma[0] not in dic_lemmas:
            dic_lemmas[lemma[0]] = {}
        if lemma[:x] in dic_lemmas[lemma[0]]:
            dic_lemmas[lemma[0]][lemma[:x]].append(lemma[x+1:])
        else:
            dic_lemmas[lemma[0]][lemma[:x]] = []
            try:
                if lineSplit[-1] != "":
                    dic_lemmas[lemma[0]][lemma[:x]].append(lineSplit[-1])
                else:
                    dic_lemmas[lemma[0]][lemma[:x]].append(lineSplit[-2])
            except IndexError:
                print(x)
texto = getCorpus('e960401.htm', 'latin-1')
texto2 = cleanTokens3(texto)
Lemmas(texto2)