# -*- coding: utf-8 -*-
"""
analiza el texto que contiene las lematizaciones, despues procede a eliminar los
caracteres no deseados para el analisis, luego atraves del diccionario de lemas
coloca su forma primal de las palabras, al final se eliminan las stopwords
dejando un texto limpio para proceder a analisis

"""

import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import time
import re
import unicodedata

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
    print("Lematizando...")
    palabra_lemmatizada = ""
    listEscritura = []
    for word in vocabulario:
        palabra_lemmatizada = "(" +word + ")  \n"
        dic_temporal = dic_lemmas[word[0]]
        for key in dic_temporal:
            if word.startswith(key):
                for i in range(0,len(dic_temporal[key]["Terminaciones"])):
                    if(word == dic_temporal[key]["Palabra"]):
                        palabra_lemmatizada = "(" + dic_temporal[key]["Palabra"]+ " | " + dic_temporal[key]["Classificiacion"] +") \n "
                        break
                    if len(dic_temporal[key]["Terminaciones"]) > 0:
                        stringtem = key + dic_temporal[key]["Terminaciones"][i]
                        if(word == stringtem):
                            palabra_lemmatizada = "(" + dic_temporal[key]["Palabra"]+ " | " + dic_temporal[key]["Classificiacion"] +") \n "
                            break
        listEscritura.append(palabra_lemmatizada)
    return listEscritura
    

def deleteStopWords(vocabulario):
    textoSW = getCorpus('stopwords_es.txt', 'utf-8') 
    sw = cleanTokens3(textoSW)
    new_v = []
    for word in vocabulario:
        if word not in sw:
            new_v.append(word)            
    return new_v

            
file=open("generate.txt", encoding="latin-1")
temp=file.read()
file.close()

lin = temp.split("\n")
lin = lin[19:]
dic_lemmas = {}
LemmaAnterior = ""
for line in lin:
    lineSplit = line.split(" ")
    #print(lineSplit)
    classificacion = [wrd for wrd in lineSplit if (wrd != '' and wrd[0].isupper()) ]
    if len(lineSplit) > 1:
        lemma = lineSplit[0]
        x = lemma.find("#") #numero de indice del hash dentro de la linea
        if lemma[0] not in dic_lemmas: #vocales {a:....}
            dic_lemmas[lemma[0]] = {}
        if lemma[:x] in dic_lemmas[lemma[0]] and lemma[x+1:] != '':
            dic_lemmas[lemma[0]][lemma[:x]]["Terminaciones"].append(lemma[x+1:])
        else:
            dic_lemmas[lemma[0]][lemma[:x]] = {}
            dic_lemmas[lemma[0]][lemma[:x]]["Terminaciones"] = []
            dic_lemmas[lemma[0]][lemma[:x]]["Classificiacion"] = classificacion[0].lower()
            try:
                if lineSplit[-1] != "":
                    dic_lemmas[lemma[0]][lemma[:x]]["Palabra"] = lineSplit[-1]
                else:
                    dic_lemmas[lemma[0]][lemma[:x]]["Palabra"] = lineSplit[-2]
            except IndexError:
                print(x)
        #print(lemma[0],":",dic_lemmas[lemma[0]][lemma[:x]])
        
texto = getCorpus('e960401.htm', 'latin-1')
texto2 = cleanTokens3(texto)
#print(dic_lemmas["a"]["autoridad"])
texto3 = deleteStopWords(texto2)
texto4 = Lemmas(texto3)


file=open("lemma.txt", "w")
file.write(" ".join(texto4))
file.close()