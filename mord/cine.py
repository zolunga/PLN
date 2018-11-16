#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 15:11:19 2018

@author: alan
"""
import mord as m
import numpy as np
from xml.dom import minidom
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
def getRankXML(rawXML, nameXML):
    try:
        xml = minidom.parseString(rawXML)
        review = xml.getElementsByTagName('review')
        return review[0].attributes['rank'].value
    except Exception as e:
        print("Lectura fallida en", nameXML, "--", e)
        return 0
    
def getLemmas(text):
    lemmas = ""
    lines = text.split("\n")
    for line in lines:
        try:
            #print((line.split(" "))[1])
            lemmas += (line.split(" "))[1] + " "
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

categories = []
text = []
fails = 0
for i in range(2,4280):  #4280
    path1 = 'corpus/' + str(i) + '.xml'
    path2 = 'corpus/' + str(i) + '.review.pos'
    
    rawXML = getTemcorpus(path1,'latin-1')
    rawText = getTemcorpus(path2,'latin-1')
    
    if rawXML == False or rawText == False:
        fails += 1
        continue
    categories.append(int(getRankXML(rawXML, path1)))
    text.append(getLemmas(rawText))      

print("Total de errores:", fails)

countOBJ = CountVectorizer() #ser de magia :v
tfidfOBJ = TfidfTransformer() #ser de magia :v
x_count = countOBJ.fit_transform(text)
x_tdidf = tfidfOBJ.fit_transform(x_count)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
                                   x_tdidf, np.array(categories), test_size=0.2)

mordObj = m.LogisticIT()
mordObj.fit(x_tdidf, np.array(categories))

y_pred = mordObj.predict(X_test)

from sklearn import metrics
from sklearn.metrics import confusion_matrix
print('Accuracy of prediction is', mordObj.score(X_test, y_test))
print('Confusion matrix:\n', confusion_matrix(y_test, y_pred))
print(metrics.classification_report(y_test, y_pred))
