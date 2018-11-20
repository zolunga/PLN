# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 20:11:43 2018

@author: Alan
"""
import pickle

file=open("generate.txt", encoding="latin-1")
temp=file.read()
file.close()
conTeoSust = [] 
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

file = open('dictionary', 'wb')
pickle.dump(dic_lemmas, file)
file.close()
