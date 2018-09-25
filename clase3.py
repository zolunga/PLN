#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:55:01 2018

@author: alan
"""
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import operator
import numpy as np
import math
import re
from nltk.corpus import cess_esp
print(cess_esp)
cess_esp_tagged_sents = cess_esp.tagged_sents()
print(cess_esp_tagged_sents)
#cess_esp_sents = cess_esp.sents(categories='news')