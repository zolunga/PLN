# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 16:01:48 2018

@author: xboxh
"""
#import TratamientoTexto.py
from nltk import word_tokenize
import nltk
import operator
import numpy as np
import math
import re
import time
import unicodedata
from bs4 import BeautifulSoup

from nltk.corpus import cess_esp
from pickle import dump, load
#from write import writeDict
dic_sustantivos={}

def main():
    #generatizar()
    arti=split_into_articles('Corpus/e960401.htm')
    #train_lematizador()
    #train_and_save_spanish_tagger()
    for art in arti:
        s=quitarSpTex(art)
        sent_text=nltk.sent_tokenize(s)
        text_tagged=tag_spanish_sentences(sent_text)
        lema_text=Lemma_tagged_text(text_tagged)
    SustMasUsado()
        #print (lema_text)
        
        
        

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



def Lemma_tagged_text(tag_text):
    lematizador=Cargar_lematizador()
    new_lemma_tag_text=[]
    dic_sustantivos_Art={}
    global dic_sustantivos
    for sentece in tag_text:
        for tupla in sentece:
            
            #cosa = "";
            if(tupla[0] in lematizador):
                #Nuevatupla=lematizador[tupla[0]]
                new_lemma_tag_text.append(lematizador.get(tupla[0]))
                Nuevatupla=lematizador.get(tupla[0])
                #print("lematice!",tupla[0],Nuevatupla[0])
            else:
                #Nuevatupla=tupla
                new_lemma_tag_text.append(tupla)
                Nuevatupla=tupla
            
            #print (Nuevatupla)    
            if 'nc' in str(Nuevatupla[1]):
                #print ("sustantivo!",Nuevatupla)
                if(  (Nuevatupla[0] not in dic_sustantivos)):
                    dic_sustantivos[Nuevatupla[0]] = 0
                
                if(  (Nuevatupla[0] not in dic_sustantivos_Art)):
                    dic_sustantivos_Art[Nuevatupla[0]] = 0
                dic_sustantivos[Nuevatupla[0]]+=1
                dic_sustantivos_Art[Nuevatupla[0]]+=1
                
                #if(Nuevatupla[0] == 'arquitectura'):
                #    print("aparecio")
    
    FinaldeArticulo = "Sustantivos: "
    Total = 0
    #if ('arquitectura' in dic_sustantivos_Art ):
    #    print('ya esta')  
    SustAnalizar=['inmigración','arquitectura','internet','astronauta','inflación']
    for key in dic_sustantivos_Art:
        #Total += dic_sustantivos[key]
        Total += dic_sustantivos_Art[key]
    for key in dic_sustantivos_Art:
        #dic_sustantivos[key] = round( (dic_sustantivos[key] / Total) * 100, 2)
        dic_sustantivos_Art[key] = round( (dic_sustantivos_Art[key] / Total) , 4)
    #dic_sustantivos = sorted(dic_sustantivos.items(), key=operator.itemgetter(1))
    #if ('arquitectura' in dic_sustantivos_Art ):
    #    print('ya esta')
    FinaldeArticulo+="\t".join(SustAnalizar)
    FinaldeArticulo+="\n\t\t"
    for key in SustAnalizar:
        
        if key in dic_sustantivos_Art:
            #FinaldeArticulo+=str(a)
            #FinaldeArticulo+=str(b)
            #print ('entre')
            FinaldeArticulo+=str(dic_sustantivos_Art[key])
        else:
            FinaldeArticulo+=str(0)
            FinaldeArticulo += "\t\t"
            
    dic_sustantivos_Art = sorted(dic_sustantivos_Art.items(), key=operator.itemgetter(1))
    #print (dic_sustantivos_Art[0:10])
    #new_dic_sust={}
    #for a,b in dic_sustantivos_Art:
    #    new_dic_sust[a]=b
        
        
   
        
            
            
    
    #FinaldeArticulo += str(dic_sustantivos[len(dic_sustantivos)-4:])
    
    
    FinaldeArticulo += "\n"
    print (FinaldeArticulo)
    
    return new_lemma_tag_text
    
        
            



def Cargar_lematizador():
    fname='ini.pk1'
    input = open(fname,'rb')
    lemati=load(input)
    input.close()
    return lemati


def train_lematizador():
    ini=inicializarlematizador()
    fname='ini.pk1'
    output=open(fname,'wb')
    dump(ini,output,-1)
    output.close()
    
           
            
def inicializarlematizador():
    import string
    #dict_Lemma={}
    dic_letra={}
    for letra in string.ascii_lowercase[:32]:
        t=leerAr("Generate/"+letra+"_generate")
        t=t.split("\n")
        #dic_letra={}
        for w in t:
            if(w!=''):
                w=w.split(" ")
                #print (w)
                dic_letra[w[0]]=(w[1],w[2])
        #dict_Lemma[letra]=dic_letra    
        
    return dic_letra#dict_Lemma
            
            
   
        

def quitarSpTex(ts):
    tokens = Tokenizar(ts)
    tokens=EliminarStopWords(tokens)
    text= " ".join(tokens)
    return text
    

def main3():
    
    tS=LeerArchivo()
    sent_text = nltk.sent_tokenize(tS)
    print (sent_text[12])
    tokenized_text = nltk.word_tokenize(sent_text[12])
    tagged = nltk.pos_tag(tokenized_text)
    print(tagged)
    
    #brown_tagged_sents = brown.tagged_sents(categories='news')
    #brown_sents= brown.sents(categories='news')
    train_and_save_spanish_tagger()
    
    '''
    cess_esp etiquetado en español
    Freeling el mejor para español
    '''
    #artz= split_into_articles("Corpus/e960401.htm")
    #artz=artz [:1]
    
    
    #print (len(artz),artz[:1])
    
    
def tag_spanish_sentences(sentences):
    fname='UnigramTagger_cess_esp.pk1'
    input = open(fname,'rb')
    tagger=load(input)
    input.close()
    sentences_taged=[]
    for s in sentences:
        tokens=nltk.word_tokenize(s)
        s_tagged=tagger.tag(tokens)
        sentences_taged.append(s_tagged)
        #print(s_tagged)
    return sentences_taged

    

def train_and_save_spanish_tagger():
    cess_tagged_sents=cess_esp.tagged_sents()
    tagger=nltk.UnigramTagger(cess_tagged_sents)
    fname='UnigramTagger_cess_esp.pk1'
    output=open(fname,'wb')
    dump(tagger,output,-1)
    output.close()
    


def main2 ():
    tS=LeerArchivo()
    tokens = Tokenizar(tS)
    
    #tok=tokens.collocations()
    #print(tok)
    
    
    
    tokens= CleanTokens(tokens)
    #tokens_nltk = nltk.Text(tokens)
    print("Cantidad:",len(tokens))
    tokens= EliminarStopWords(tokens)
    print("Cantidad:",len(tokens))
    
    Vocabulario = get_vocabulary(tokens)
    #print (Vocabulario[:10])
    #$print (''.join((c for c in unicodedata.normalize('NFD',"ó") if unicodedata.category(c) != 'Mn')))
    #return
    #generatizar()
    lematizar2(tokens,Vocabulario)
    #lematizado=lematizas(tokens,Vocabulario)
    #toke=Tokenizar(lematizado)
    #print (len(get_vocabulary(toke)), "antes", len(Vocabulario))
    #print(toke[:10])
    #guardarArchivo("tokensnuevos",toke) 
    
    
    
    
    '''
    contextos=retrieve_contexts(tokens,Vocabulario,8)
    #print(contextos["empresa"])
    #Obtener Vectoresde frecuencia
    #print(contextos[:10])
    raw_Vectors=raw_freq_vectors(Vocabulario,contextos)
    #print (raw_Vectors[:30])
    similares=cosine_similarity(raw_Vectors,"empresa")
    
    for w in similares:
        print (w)
    
   
    #print("Palbaras similares")
    pass'''
    
    
def split_into_articles(fname):
    f=open(fname, 'r', encoding='latin-1') 
    t=f.read()
    f.close()
    text=t.replace(u'\x97', '') 
 
    #articles=re.split('<h3>', text) #articles is a list of strings
    articles=re.split(r'http://www.excelsior.com.mx/9604/960401/[\w]{3}[\d]{2}.html', text)
    arts=[]
    for article in articles:
        soup = BeautifulSoup(article, 'lxml') #article is a string
        text = soup.get_text()
        text=text.replace(u'\x97', '')
        arts.append(text)
     
    return arts #a list of strings, each string is an article


def QuitaAcento(s):
    return ''.join((c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c) != 'Mn'))
def generatizar():
    import unicodedata
    f=open('generate.txt', encoding='latin-1')
    t=f.read()
    f.close()
    t=t.split("\n")
    
    j=0
    conjunto=[]
    letra='a'
    for p in t[18:len(t)-5]:
        j+=1;
        if(j==5000):
            print (".")
            j=0
        
        #print (p)
        palabras=p.split(" ")
        
        #print (palabras)
        #ini =input()
        #time.sleep(1)
        palare=palabras[0].replace("#","")
        
        linea=""
        if(palare!=""):
            letrita=''.join((c for c in unicodedata.normalize('NFD',palabras[0][0]) if unicodedata.category(c) != 'Mn'))
            
            if(palabras[len(palabras)-1]==''):
                linea=palare+" "+palabras[len(palabras)-2]+" "+palabras[len(palabras)-3].lower()
            else:
                linea=palare+" "+palabras[len(palabras)-1]+" "+palabras[len(palabras)-2].lower()
            
            if(letrita==letra):
                conjunto.append(linea)
            else:
                print("Voy a cabiar: ",letra)
                guardarArchivo("Generate/"+letra+"_generate",conjunto,"a")
                letra=letrita
                print(letra)
                conjunto=[]
                conjunto.append(linea)
    guardarArchivo("Generate/"+letra+"_generate",conjunto,"a")
        
    #return text;
    

def guardarArchivo(nombre,cosa,forma):
    f = open (nombre,forma)
    for w in cosa:    
        f.write(w+"\n")
    f.close()
    
   
def cambiaPalabras(protopatron,palabra,text):
    
    palabra= palabra.split(" ")[1]
    #print("cambiare ",protopatron,"por: ",palabra)
    #time.sleep(1)
    text=text.replace(" "+protopatron+" "," "+palabra+" ")
    return text
    

def leerAr(nombre):
    f=open(nombre, encoding='latin-1')
    t=f.read()
    f.close()
    return t


def lematizar2(texto,vocabulario):
    Letra="a"
    t=leerAr("Generate/"+Letra+"_generate")
    t=t.split("\n")
    texto=" ".join(texto)
    
    st= []
    for w in t:
        w=w.split(" ")
        st.append(w[0])
    
    #print (st)
    
    for w in vocabulario:
         if(w!=''):   
            if(QuitaAcento( w[0])!=Letra):
                Letra=QuitaAcento( w[0])
                t=leerAr("Generate/"+Letra+"_generate")
                t=t.split("\n")
                st= []
                for w in t:
                    w=w.split(" ")
                    st.append(w[0])
            if(w in st):
                texto=cambiaPalabras(w, t[st.index(w)],texto)
                #print (texto[:1000])
        
        
            
    guardarArchivo( "NuevoTexto",texto.split("\n"))
    print("Acabe!")
        
        

def lematizas(text,vocabulario):
    f=open('generate.txt', encoding='latin-1')
    t=f.read()
    f.close()
    t=t.split("\n")
    text= (" ").join(text)
    vaca= (" ").join(vocabulario)
    j=0
    for p in t[19:len(t)-5]:
        j+=1;
        if(j==5000):
            print (".")
            j=0
        
        #print (p)
        palabras=p.split(" ")
        
        #print (palabras)
        #ini =input()
        #time.sleep(1)
        #patron=palabras[0].replace("#","[a-z]{1,2}")
        patron=palabras[0].replace("#","")
        if(palabras[len(palabras)-1]==''):
            text=cambiaPalabras(patron,text,palabras[len(palabras)-2],vaca)
        else:
            text=cambiaPalabras(patron,text,palabras[len(palabras)-1],vaca)
    
    return text;
    
    

def retrieve_contexts(text, vocabulary, windowSize):
    
    contextDict={}
    for w in vocabulary:
        context=[]
        for i in range(len(text)):
            if text[i]==w:
                for j in range(i-int(windowSize/2), i): #left context
                    if j >= 0:
                        context.append(text[j])
                try:
                    for j in range(i+1, i+(int(windowSize/2)+1)): #right context
                        context.append(text[j])
                except IndexError:
                    pass
        
        contextDict[w]=context
        #print(contextDict[w])
 
    return contextDict


def cosine_similarity(raw_freq_vectors_dict, word):
    similar_words_dict={}
    vector_to_compare=raw_freq_vectors_dict[word]
    v_to_compare=np.array(vector_to_compare)
     
    vc_squared=v_to_compare**2
    vc_sum=vc_squared.sum()
    vc_length=math.sqrt(vc_sum) 
     
    i=0
    for key in raw_freq_vectors_dict.keys():
        v=np.array(raw_freq_vectors_dict[key])
        print (v) 
        v_squared=v**2
        print (v_squared)
        v_sum=v_squared.sum()
        print(v_sum)
        v_length=np.sqrt(v_sum) 
        lengths_product=vc_length*v_length
        num=np.dot(v_to_compare, v)/lengths_product
        print ("cosaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",num)
        similar_words_dict[key]=num        
        i+=1
        print('cosine_similarity function ', str(i), str(similar_words_dict[key]))
     
    similar_words = sorted(similar_words_dict.items(), key=operator.itemgetter(1), reverse=True)
    return similar_words



def raw_freq_vectors(voca, contexts):
    #f_vocabulary=open(fname_vocabulary, encoding='utf-8')
    #voc=f_vocabulary.read()
    vocabulary=voca
    #f_vocabulary.close()
     
    #f_contexts=open(fname_contexts, encoding='utf-8')
    #contexts=f_contexts.readlines()
    #f_contexts.close()
     
    raw_freq_vectors_dict={}
    #raw_freq_vectors_dict.
    for context in contexts:
        if(context!=''):
            print ("El contexto es",context)
            words=context.split()
            vector=[]
            for voc in vocabulary:
                vector.append(words[1:].count(voc))
            #raw_freq_vectors_dict.SetItem(vector)
            #if(len(words)>0):
            raw_freq_vectors_dict[words[0]]=vector
            #print('raw_frequency_vectors function ', str(contexts.get(context)))

    return raw_freq_vectors_dict


def LeerArchivo():
    
    f=open('Corpus/e960401.htm', encoding='latin-1')
    t=f.read()
    f.close()
     
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tS = tS.replace('\x97', ' ')
    tS = tS.lower()
    return tS

def Tokenizar(tS):
    
    tokens = nltk.Text(  word_tokenize(tS) )   
    return tokens


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
    print('Hay', len(tokenslimpios),'tokens')
    return tokenslimpios
       

def EliminarStopWords(tokens):
    f=open('stopwords_es.txt', encoding='utf-8')
    t=f.read()
    f.close()
    StopW = nltk.Text(  word_tokenize(t) )
    
    #print(StopW[:10])
    tokensLimpios=[]
    for w in tokens:
        if w not in StopW:            
            tokensLimpios.append(w)
            #print(w)
    return tokensLimpios

def get_vocabulary(alist):
    vocabulary=sorted(set(alist))
    print('There are', len( vocabulary), 'words in  vocabulary.\n')
    return vocabulary

def ObtenerContextos(text, vocabulary, windowSize):
    
    contextDict={}
    for w in vocabulary:
        context=[]
        for i in range(len(text)):
            if text[i]==w:
                for j in range(i-int(windowSize/2), i): #left context
                    if j >= 0:
                        context.append(text[j])
                try:
                    for j in range(i+1, i+(int(windowSize/2)+1)): #right context
                        context.append(text[j])
                except IndexError:
                    pass
            contextDict[w]=context 
     
    return contextDict




def conditional_entropy(pW1_1, pW2_1, pW1_1W2_1):
    pW2_0   = 1-pW2_1
    pW1_1W2_0 = pW1_1 - pW1_1W2_1
    pW1_0W2_0 = pW2_0 - pW1_1W2_0
    pW1_0W2_1 = pW2_1 - pW1_1W2_1
    if pW1_0W2_0>0 and pW1_0W2_1>0 and pW1_1W2_0>0 and pW1_1W2_1>0:
        condEntropy=(pW1_0W2_0*math.log(pW2_0/pW1_0W2_0, 2))+\
                       (pW1_1W2_0*math.log(pW2_0/pW1_1W2_0, 2))+\
                            (pW1_0W2_1*math.log(pW2_1/pW1_0W2_1, 2))+\
                              (pW1_1W2_1*math.log(pW2_1/pW1_1W2_1, 2))
    else:
        condEntropy=0
    return condEntropy
 
 
def get_sentences(text_string):
    sent_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    sentences=sent_tokenizer.tokenize(text_string)
    print('There are', len(sentences), 'sentences.')
    return sentences
def cos():
    if __name__=='__main__':
        fname='e960401.html'
        text_string=get_text_string(fname)
        raw_tokens=get_raw_tokens(text_string)
        clean_tokens=get_clean_tokens(raw_tokens)
        fname_stopwords='stopwords_es.txt'
        tokens_without_stopwords=delete_stopwords(fname_stopwords, clean_tokens)
        vocabulary=get_vocabulary(tokens_without_stopwords) 
        
        sentences=get_sentences(text_string)
        N=len(sentences)
        
        pW2_1=[]
        for W2 in vocabulary:
            freq=0
            for sent in sentences:
                if W2 in sent:
                    freq+=1
            pW2_1.append(freq/N)
              
        W1='empresa'
        index=vocabulary.index(W1)
        pW1_1=pW2_1[index]
        
        pW1_1W2_1=[]
        for W2 in vocabulary:
            freq=0
            for sent in sentences:
                if W1 in sent and W2 in sent:
                    freq+=1
            pW1_1W2_1.append(freq/N)
              
        cond_entropy={}
        for i in range(len(vocabulary)):
            cond_ent=conditional_entropy(pW1_1, pW2_1[i], pW1_1W2_1[i])
            if cond_ent:
                cond_entropy[vocabulary[i]]=cond_ent
         
        sorted_entropy=sorted(cond_entropy.items(), key=operator.itemgetter(1))
        writeList(sorted_entropy, 'empresa_cond_entropy.txt')



if __name__== "__main__":
    main()