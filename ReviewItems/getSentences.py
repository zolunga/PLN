#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 15:25:58 2018

@author: alan
"""
import nltk

def GetCorpusC(NameDoc,encode):
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
    Sentences =  nltk.Text(nltk.sent_tokenize(tS))
    return Sentences 

def getAllReviews():
    TemporalName1 = ""
    TemporalName2 = ""
    Temporaltext = []
    texts = {}
    for i in range(0,6): #0, 6
        for j in range (0, 30):  #0, 30
            TemporalName1 = "moviles/no_" + str(i) + "_" + str(j) + ".txt"
            TemporalName2 = "moviles/yes_" + str(i) + "_" + str(j) + ".txt"
            Temporaltext = GetCorpusC(TemporalName1, 'latin-1')
            if len(Temporaltext) > 0:
                texts[TemporalName1[8:]] = Temporaltext
                
            Temporaltext = GetCorpusC(TemporalName2, 'utf-8') 
            if len(Temporaltext) > 0:
                texts[TemporalName2[8:]] = Temporaltext
    return texts
