#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 15:11:19 2018

@author: alan
"""
#import mord as m
from bs4 import BeautifulSoup
from xml.dom import minidom
import time

def getRankXML(rawXML, nameXML):
    rawXML.replace("&", "")
    try:
        xml = minidom.parseString(rawXML)
        review = xml.getElementsByTagName('review')
        return review[0].attributes['rank'].value
    except Exception as e:
        print("Lectura fallida en", nameXML, "--", e)
        return 0
def getLemmas(text):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
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
        t.replace("&", "")
        return t
    except: 
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
    
    categories.append(getRankXML(rawXML, path1))
    text.append(getLemmas(rawText))      

print("Total de errores:", fails)
#print(categories)
#print(text)

