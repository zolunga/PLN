# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 20:37:33 2018

@author: Alan
"""

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
import operator
dic_sustantivo = {}

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
        tS = soup.get_text()
        tS = tS.replace('\x97', ' ')
        tS = tS.replace('-', ' ')
        tS = tS.replace('¿', ' ')
        tS = tS.replace('?', ' ')
        tS = tS.replace('!', ' ')
        tS = tS.replace('¡', ' ')
        tS = tS.lower()
        ArticlesClean.append(tS)
    return ArticlesClean

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
    #print("cleanTokens terminado")
    #time.sleep(2)
    return Arr

def Lemmas(vocabulario):
    print("Lematizando...")
    global dic_sustantivo
    palabra_lemmatizada = ""
    listEscritura = []
    for word in vocabulario:
        palabra_lemmatizada = "(" + word + ")  \n"
        dic_temporal = dic_lemmas[word[0]]
        for key in dic_temporal:
            if word.startswith(key):
                if(word == dic_temporal[key]["Palabra"]):
                    palabra_lemmatizada = "(" + dic_temporal[key]["Palabra"]+ " | " + dic_temporal[key]["Classificiacion"] +") \n"
                    #-------------------sustantivo
                    if dic_temporal[key]["Classificiacion"].startswith("nc"):
                        if dic_temporal[key]["Palabra"]  not in dic_sustantivo:
                            dic_sustantivo[dic_temporal[key]["Palabra"]] = {}
                            dic_sustantivo[dic_temporal[key]["Palabra"]]['Conteo'] = 1
                            dic_sustantivo[dic_temporal[key]["Palabra"]]['Articulo'] 
                        else:
                            dic_sustantivo[dic_temporal[key]["Palabra"]] += 1
                    #----------------------------
                    
                for i in range(0,len(dic_temporal[key]["Terminaciones"])):
                    if len(dic_temporal[key]["Terminaciones"]) > 0:
                        stringtem = key + dic_temporal[key]["Terminaciones"][i]
                        if(word == stringtem):
                            #-------------------sustantivo
                            if dic_temporal[key]["Classificiacion"].startswith("nc"):
                                if dic_temporal[key]["Palabra"]  not in dic_sustantivo:
                                    dic_sustantivo[dic_temporal[key]["Palabra"]] = 1
                                else:
                                    dic_sustantivo[dic_temporal[key]["Palabra"]] += 1
                            #----------------------------
                            palabra_lemmatizada = "(" + dic_temporal[key]["Palabra"]+ " | " + dic_temporal[key]["Classificiacion"] +") \n"
                            break
        listEscritura.append(palabra_lemmatizada)
    #print(sorted_d)
    #FinaldeArticulo = "Sustantivos mas usados: "
    #Total = 0
    #for key in dic_sustantivo:
    #    Total += dic_sustantivo[key]
    #for key in dic_sustantivo:
    #    dic_sustantivo[key] = round( (dic_sustantivo[key] / Total) * 100, 2)
    #dic_sustantivo = sorted(dic_sustantivo.items(), key=operator.itemgetter(1))
    #FinaldeArticulo += str(dic_sustantivo[len(dic_sustantivo)-4:])
    
    '''
    for word in dic_sustantivo:
        if dic_sustantivo[key] > 1:
            porcentaje = round( (dic_sustantivo[key] / Total) * 100, 2)
            FinaldeArticulo += key + ":" + str(porcentaje) + "% ----"
    '''
    #FinaldeArticulo += "\n"
    #listEscritura.append(FinaldeArticulo)
    #print(listEscritura)
    #time.sleep(3)
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
            dic_lemmas[lemma[0]][lemma[:x]]["Terminaciones"].append(lemma[x+1:])
            try:
                if lineSplit[-1] != "":
                    dic_lemmas[lemma[0]][lemma[:x]]["Palabra"] = lineSplit[-1]
                else:
                    dic_lemmas[lemma[0]][lemma[:x]]["Palabra"] = lineSplit[-2]
            except IndexError:
                print(x)
        #print(lemma[0],":",dic_lemmas[lemma[0]][lemma[:x]])        
        
texto = getRawCorpus('e960401.htm', 'latin-1')
Articulos = getArticles(texto)        
file=open("lemma.txt", "w")
for i in range(0, len(Articulos)):
    listaPalabrasArt = Articulos[i].split(" ")
    textoTemporal = cleanTokens3(listaPalabrasArt)
    textoTemporal = deleteStopWords(textoTemporal)
    textoTemporal = Lemmas(textoTemporal)
    file.write("----------------------------Articulo ----------------------\n")
    file.write(" ".join(textoTemporal))    

#print(dic_lemmas['m']['millón'])
Total = 0
for key in dic_sustantivo:
    Total += dic_sustantivo[key]
#for key in dic_sustantivo:
#    dic_sustantivo[key] = round( (dic_sustantivo[key] / Total) * 100, 2)
dic_sustantivo = sorted(dic_sustantivo.items(), key=operator.itemgetter(1))
print(dic_sustantivo)
    

file.close()