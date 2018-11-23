# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 15:33:42 2018

@author: xboxh
"""

from xml.dom import minidom
from bs4 import BeautifulSoup

def getRankXML(rawXML, nameXML):
    try:
        xml = minidom.parseString(rawXML)
        review = xml.getElementsByTagName('review')
        return review[0].attributes['rank'].value
    except Exception as e:
        #print("Lectura fallida en", nameXML, "--", e)
        return 0
    
def getLemmas(text):
    lemmas = []
    lines = text.split("\n")
    for line in lines:
        try:
            #print((line.split(" "))[1])
            lemmas.append( (line.split(" "))[1] )
        except:
            continue
    return lemmas

def getTemcorpus(NameDoc, encode):
    
    try:
        f=open(NameDoc, encoding=encode)
        t=f.read()
        f.close()
        if("xml" in NameDoc):
            t = t.replace('&', '')
        return t
    except Exception as e:
        #print("Corpus:",NameDoc,"-", e)
        return False

def getSentimentalDictionary():
    dict1 = {}
    doc = open('fullStrengthLexicon.txt', encoding='utf-8')
    contents = doc.read()
    contents = contents.split("\n")
    for line in contents:
        pala=line.split("\t")
        #print (line,"---",pala)
        dict1[pala[0]] = pala[len(pala)-1] 
        
    
    #soup = BeautifulSoup(contents,'lxml')
    #sentimientos = soup.find_all('lemma')
    #for i in range(0, len(sentimientos)):
    #    dict1[sentimientos[i].text[1:-1]] = sentimientos[i].get('pol')
    return dict1



def elimina_tildes(cadena):
    import unicodedata
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s


def analizeText(Text, Dict, Keys):#Cuenta cantidad de pos y neg
    summ =[0,0]
    for words in Text:
        word=elimina_tildes(words)
        if word in Keys:
            if(Dict[word]=="pos"):
                summ[0]+=1;
            if(Dict[word]=="neg"):
                summ[1]+=1;
            
    return summ


sentimental_dict = getSentimentalDictionary()
text_dict = {}
Sents = list(sentimental_dict.keys())
sumCategories = {
                'cat1': { 'cant':0, 'sumPos':0, 'sumNeg':0},
                'cat2': { 'cant':0, 'sumPos':0, 'sumNeg':0},
                'cat3': { 'cant':0, 'sumPos':0, 'sumNeg':0},
                'cat4': { 'cant':0, 'sumPos':0, 'sumNeg':0},
                'cat5': { 'cant':0, 'sumPos':0, 'sumNeg':0},
                }
for i in range(2,4280):  #4280
    path1 = 'corpus/' + str(i) + '.xml'
    path2 = 'corpus/' + str(i) + '.review.pos'
    
    rawXML = getTemcorpus(path1,'latin-1')
    rawText = getTemcorpus(path2,'latin-1')
    
    if rawXML == False or rawText == False:
        continue
    textRev = getLemmas(rawText)
    PosNeg=analizeText(textRev, sentimental_dict, Sents)
    text_dict[str(i)] = {
                        'cat':getRankXML(rawXML,path1), 
                        'sumPos':PosNeg[0],
                        'sumNeg':PosNeg[1]
                        }
    if(i%500==0):
        print(i)
    



for key in text_dict:
    if text_dict[key]['cat'] == 0:
        continue
    cat = 'cat' + str(text_dict[key]['cat'])
    sumCategories[cat]['cant'] += 1
    sumCategories[cat]['sumPos'] += text_dict[key]['sumPos']
    sumCategories[cat]['sumNeg'] += text_dict[key]['sumNeg']

for g in sumCategories:
    print(sumCategories[g])
    #print("promedio positivo: ",sumCategories[g]['sumPos']/sumCategories[g]['cant'],"\nPromedio Negativo",sumCategories[g]['sumNeg']/sumCategories[g]['cant'])


#print(sumCategories)
