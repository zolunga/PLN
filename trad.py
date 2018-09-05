#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 15:22:48 2018

@author: alan
"""
from nltk.corpus import swadesh
from nltk.corpus import wordnet as wn

es2en = swadesh.entries(['es', 'en'])
translate = dict(es2en)
#print(es2en)

arr = ['cenizas','nieve','hincharse']
#for word in arr:
#    print(word,"----",translate[word])
    
    
#print(wn.synsets('computer'))    
#print(wn.synset('computer.n.01').lemma_names())
#print(wn.synset('computer.n.01').definition())



computadora = wn.synsets('computer.n.01')
x = computadora.hypernyms()
#print("hyp-",computadora.hyponyms())
#print("hyp-",computadora.hypernyms())
print(x)