# -*- coding: utf-8 -*-


import nltk
import pickle
import re
import json
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
import operator
from nltk.corpus import PlaintextCorpusReader
import chukinize as chu

def getCorpus(NameDoc, encode):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
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
    tokens =  nltk.Text(nltk.word_tokenize(tS))
    return tokens


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
    #tokens =  nltk.Text(nltk.word_tokenize(tS))
    return tS
    

def cleanTokens(vocabulario):
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
    return Arr

def deleteStopWords(vocabulario, sw):
    new_v = []
    for word in vocabulario:
        if word not in sw:
            new_v.append(word)            
    return new_v

def loadLemmaDict():
    file = open('dictionary', 'rb')
    dictionary = pickle.load(file)
    file.close()
    return dictionary

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

def lemmatizado(text, lemmas):
    new_text = []
    for word in text:
        dictLetter = lemmas[word[0]]
        for key in dictLetter:
            for Terminacion in dictLetter[key]['Terminaciones']:
                combinacion = key + "" + Terminacion
                if combinacion == word:
                    new_text.append({'Palabra':dictLetter[key]['Palabra'],
                                     'tipo': dictLetter[key]['Classificiacion']})
                    break
        new_text.append({'Palabra': word,
                         'tipo': "sn"})
    return new_text

def SustMasUsado():
    FinaldeArticulo = "Sustantivos mas usados: "
    Total = 0
    global dic_sustantivos
    for key in dic_sustantivos:
        Total += dic_sustantivos[key]
    for key in dic_sustantivos:
        dic_sustantivos[key] = round( (dic_sustantivos[key] / Total) * 100, 2)
    dic_sustantivos = sorted(dic_sustantivos.items(), key=operator.itemgetter(1))
    FinaldeArticulo += str(dic_sustantivos[len(dic_sustantivos)-4:])
    
    
    FinaldeArticulo += "\n"
    print (dic_sustantivos)



def compute_ngrams(sequence,n):
    return zip(*[sequence[index:] for index in range (n)])


def get_top_ngrams(corpus,ngram_vals=1,limit=5):
    import operator
    tokens = corpus#nltk.word_tokenize(corpus)
    
    ngrams = compute_ngrams(tokens, ngram_vals)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd= sorted(ngrams_freq_dist.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams= [(' '.join(text), freq)
                    for text, freq in sorted_ngrams]
    
    
    return sorted_ngrams
    
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

def CleanTokens(raw_tokens):
    
    patronLimpiador = re.compile("[a-zA-ZáéíóúñÑü]")
    tokenslimpios=[]
    for w in raw_tokens:
        t=[]
        for char in w:
            if(patronLimpiador.match(char)):
                t.append(char)
        letterTokens="".join(t)
        
        if(letterTokens !=" "):
            tokenslimpios.append(letterTokens)
    #print('Hay', len(tokenslimpios),'tokens')
    return tokenslimpios


def analizeText(Text, Dict, Keys):#Cuenta cantidad de pos y neg
    summ =[0,0]
    text=Text.split(" ")
    text= CleanTokens(text)
    SustNeg=""
    SustPos=""
    for word in text:
        #word=elimina_tildes(words)
        if word in Keys:
            if(Dict[word]=="pos"):
                summ[0]+=1;
                SustPos+=" "+(word)
            if(Dict[word]=="neg"):
                summ[1]+=1;
                SustNeg+=" "+(word)
            
    return summ,SustPos,SustNeg


def getPosNegAspect(sentences, aspect,dict1,keys):
    #words=sentences.split(" ")
    #print(sentences)
    re=[0,0]
    posis=""
    negis=""
    for w in sentences: 
        #words=w.split(" ")
        if(aspect in w ):
            #print(w)
            tep,pos,neg=analizeText(w,dict1,keys) 
            re[0]+=tep[0]
            re[1]+=tep[1]
            posis+=" "+pos
            negis+=" "+neg
    return re,posis,negis
            
    

def countNouns(texts):
    dictCount = {}
    for key in texts:
        for element in texts[key]:
            print(element)
            if element['tipo'].startswith("nc"):
                if element['Palabra'] in dictCount:
                    dictCount[ element['Palabra'] ] += 1
                else:
                    dictCount[ element['Palabra'] ] = 1
    return(dictCount)
    
    
def contFreq(text):
    return n


def AnalizarAspecto (Aspect):
    

    print("AnalizandoAspecto",Aspect)

    textoSW = getCorpus('stopwords_es.txt', 'utf-8') 
    sentimental_dict = getSentimentalDictionary()
    
    textoReviews = getAllReviews()
    lemmas = loadLemmaDict()
    dictionaryCount = {}
    Sents = list(sentimental_dict.keys())
    file = open('Res1.txt','w')
    conteo= [0,0]
    pos=""
    neg=""
    for key in textoReviews:
        #print(key)
        
        #print(textoReviews[key])
        sent_tokenize_list = sent_tokenize(textoReviews[key])
        chu.AnalizeSentence(sent_tokenize_list)
        
        
        
        tep,posis,negis=getPosNegAspect(sent_tokenize_list, Aspect, sentimental_dict,Sents)
        conteo[0]+=tep[0]
        conteo[1]+=tep[1]
        pos+=posis
        neg+=negis
        
        
        #print(get_top_ngrams(textoReviews[key],2,10))
        
        """
        Requiere tokenizar
        textoReviews[key] = cleanTokens(textoReviews[key])
        textoReviews[key] = deleteStopWords(textoReviews[key], textoSW)
        textoReviews[key] = lemmatizado(textoReviews[key], lemmas)
        file.write(key)
        file.write("-------------\n") 
        file.write(json.dumps(textoReviews[key]))
        file.write("-------------\n\n\n") 
    
    last = countNouns(textoReviews)
    
    last = sorted(last.items(), key=operator.itemgetter(1))
    
    print("Sust\n\n",last)
    
    file.write("------------------------conteos----------------------------")
    file.write(json.dumps(last))
    file.close()
    
    
    """
    
    #print(conteo,"\nNegativos\n",neg,"\nPositivos\n",pos)
    print("Negativos\n")
    negativos=set(neg.split(" "))
    dict1={}
    for w in negativos:
        dict1[w]=neg.count(w)
    
    dict1 = sorted(dict1.items(), key=operator.itemgetter(1))
    print (dict1)
    
    print("Positivos\n")
    
    negativos=set(pos.split(" "))
    dict1={}
    for w in negativos:
        dict1[w]=pos.count(w)
    
    dict1 = sorted(dict1.items(), key=operator.itemgetter(1))
    print (dict1)








AnalizarAspecto("manos libres")
"""
AnalizarAspecto("pantalla")
AnalizarAspecto("bateria")
AnalizarAspecto("calidad")
AnalizarAspecto("memoria")
AnalizarAspecto("precio")
AnalizarAspecto("juegos")
AnalizarAspecto("camara")




"""












