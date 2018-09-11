#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 16:01:35 2018

@author: alan
"""

import nltk
import math
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import re
import operator
from decimal import Decimal


def getCorpus(NameDoc, encode):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
    f=open(NameDoc, encoding=encode)
    t=f.read()
    
    f.close()
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tokens =  nltk.Text(nltk.word_tokenize(tS)) 
    return tokens


texto = getCorpus('e960401.htm', 'latin-1')


print("---------------------------")
print(texto.collocations())

