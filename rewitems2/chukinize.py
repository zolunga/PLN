# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:57:30 2018

@author: xboxh
"""

text="""
Los estudiantes de Escom ganaron el premio Nobel
"""

import nltk
import VerionPrograma as po



def ie_proces(doc):
    sentences = nltk.sent_tokenize(doc)
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    

def AnalizeSentence(sentence):
    #print("holo")
    sentences= po.tag_spanish_sentences(sentence)[0]
    #print("analizando sentencia:",sentence)
    grammar = "NP: {<d.+>?<n.+>*<s.+>?<n.+>}"
    tuNew=[]
    for w in sentences:
        #print("cosaaa",w)
        
        
        if(w[1]==None):
            w0=(w[0],"none")
            #w0[0]=w[0]
            #w0[1]="none"
            tuNew.append(w0)
            
        else:
            tuNew.append(w)

    cp= nltk.RegexpParser(grammar)
    #print (cp,)
    result =  cp.parse(tuNew)
    #print("\nChunk",result,"\n")
    for line in result:
        print("CHUNK", line)

if __name__== "main":
    te=[text]
    #sentence= po.tag_spanish_sentences(te)#Etiquetas None causan problemas
    #print (sentence[0])
    sentence=[('Los', 'da0mp0'), ('estudiantes', 'nccp000'), ('de', 'sps00'), ('Escom', "none"), ('ganaron', 'vmis3p0'), ('el', 'da0ms0'), ('premio', 'ncms000'), ('Nobel', 'np0000a')]
    
    grammar = "NP: {<d.+>?<n.+>*<s.+>?<n.+>}"
    
    cp= nltk.RegexpParser(grammar)
    print (cp)
    result =  cp.parse(sentence)
    print(result)
    
    result.draw()
