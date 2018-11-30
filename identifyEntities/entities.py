# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 21:09:27 2018

@author: Alan
"""
import nltk
from bs4 import BeautifulSoup
import time

def getCorpus(NameDoc, encode):
    f=open(NameDoc, encoding=encode)
    t=f.read()
    f.close()
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    #tS = tS.replace('\x97', ' ')
    #tS = tS.replace('-', ' ')
    #tS = tS.replace('¿', ' ')
    #tS = tS.replace('?', ' ')
    #tS = tS.replace('!', ' ')
    #tS = tS.replace('¡', ' ')
    #tS = tS.lower()
    sentences =  nltk.Text(nltk.sent_tokenize(tS))
    return sentences

def loadLemmaDict():
    file = open('dictionary', 'rb')
    dictionary = pickle.load(file)
    file.close()
    return dictionary


def checkEXP(exp, sentence, index):
    if index+1 < len(sentence) and ((sentence[index]['pos'] + 1) == sentence[index+1]['pos']):
        exp += " "+ sentence[index+1]['word']
        index += 1
        data = checkEXP(exp, sentence, index)
        return data
    else:
        return {'exp':str(exp), 'index':int(index), 'end': 0 }
        
    
sentences = getCorpus('e960401.htm', 'latin-1')
lista1 = []
listaTem = [] # Lista de todas las oraciones, cada oracion es = {'word': algo, 'pos': 4}
ListaMayus = [] #contiene todas las palabras que empiezan con mayuscula y entidade formadas por mas de una palabra
ListaPrimeraPalabra = [] #contiene los inicios de cada cadena
cont = 0 # Total de palabras que inician con mayus
for sen in sentences:
    tokens = nltk.word_tokenize(sen)
    listaTem = []
    for i in range(0,len(tokens)):
        if tokens[i][0].isupper():
             listaTem.append({'word':tokens[i], 'pos':i})
             cont += 1
    if len(listaTem) > 0:
        lista1.append(listaTem)

for sen in lista1:
    ListaPrimeraPalabra.append(sen[0]['word'])


for sen in lista1:
    i = 0
    while i < len(sen):
        exp = sen[i]['word']
        data = checkEXP(exp, sen, i)
        if data is not None:
            i = data['index']
            ListaMayus.append(data['exp'])
        i += 1
       
#for sen in ListaMayus:
#    print(sen)    

print(cont)
print(len(ListaMayus))
porcentajeMayus = (len(ListaMayus)/cont) * 100
print("Porcentaje palabras que inician con mayusculas",porcentajeMayus,"%") 






        