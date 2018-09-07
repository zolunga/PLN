import nltk
import math
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import re
import operator
from decimal import Decimal



#f=open('e960401.htm', encoding='latin-1')
#t=f.read()
#f.close()
 
#soup = BeautifulSoup(t, 'lxml')
#tS = soup.get_text()
#tS = tS.replace('\x97', ' ')
#tokens =  word_tokenize(tS)
#tokens_nltk = nltk.Text(tokens)
#print("Cantidad de palabras del texto:",len(tokens_nltk))
#print("Palabras diferentes:",len(set(tokens)) )
#print("---------Palbaras similares---------")
#print(tokens_nltk.similar("empresa"))
#print("------------------------------------")
#temporal = tokens_nltk.similar("empresa")
#f=open('e960401.txt', 'w')
#f.write(tS)
#f.close()

def getCorpus(NameDoc, encode):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
    f=open(NameDoc, encoding=encode)
    t=f.read()
    f.close()
    soup = BeautifulSoup(t, 'lxml')
    tS = soup.get_text()
    tS = tS.replace('\x97', ' ')
    tS = tS.replace('-', ' ')
    tS = tS.replace('¿', ' ')
    tS = tS.replace('?', ' ')
    tS = tS.replace('!', ' ')
    tS = tS.replace('¡', ' ')
    tS = tS.lower()
    tokens =  nltk.Text(nltk.word_tokenize(tS))
    return tokens
  
def hasNumber(Str):
    ''' retorna true si encuentra un numero en la cadena '''
    return any(char.isdigit() for char in Str)

def cleanTokens1(r_tokens):
    '''Limpia las plabras recorriendo cada caracter'''
    clean_token = []
    for tok in r_tokens:
        t = []
        for char in tok:
            if re.match(r'[a-z]', char):
                t.append(char)
        letterToken=''.join(t)
        if letterToken != ' ':
            clean_token.append(letterToken)
    return clean_token
            
def cleanTokens2(vocabulario):
    '''
    Limpia el vovabulario si esta ordenado y con palabras no repetidas, en 
    ese caso retorna un vovabulario limpio a partir de la letra a, sin simbolos
    '''
    vl = []#voc limp
    ve = []#voc elim
    for word in vocabulario:
        if "\\" not in word and "." not in word and not hasNumber(word):
            vl.append(word)
        else:
            ve.append(word)
    cont = 0
    for word in vl:
        if word.startswith('a'):
            break
        cont+=1
    vl = vl[cont:]
    return vl

def cleanTokens3(vocabulario):
    '''Solo limpia el vocabulario, usa una expresion regular para validar letra
    por letra y evitar que se ingresen caracteres no deseados o deconocidos en el corpus'''
    vl = []#voc limp
    palabra_limpia = "";
    for word in vocabulario:
        palabra_limpia = ""
        for letter in word:
            if re.match(r'[a-záéíóúñ]', letter):
                palabra_limpia += letter
        if palabra_limpia != "" and "www" not in palabra_limpia and "http" not in palabra_limpia:
            vl.append(palabra_limpia)
    #print(vl)
    return vl

def deleteStopWords(vocabulario,sw):
    new_v = []
    for word in vocabulario:
        if word not in sw:
            new_v.append(word)            
    return new_v

def getContext(vocabulario, palabra):
    '''
    Recibe el bocabulario completo y la palabra que va a buscar, retorna una lista
    de listas con el contexto del elemento en el texto
    '''
    ran = 4
    Contexs = []
    temp = []
    for x in range(0, len(vocabulario)):
        if vocabulario[x] == palabra:            
            for i in range((x - ran), (x + ran) ):
                if vocabulario[i] != palabra:
                    temp.append(vocabulario[i])
            Contexs.append(temp)
            temp = []
    print("Lista de contexto de ", palabra)
    print(Contexs)
    return Contexs


def createVector(vocabulario, contx):
    list_pal_con = []
    cont = 0
    for lista in contx:
        for pal in lista:
            list_pal_con.append(pal)
    vector = []
    for x in range(0, len(vocabulario)):
        for i in range(0, len(list_pal_con)):
            if vocabulario[x] == list_pal_con[i]:
                cont+=1
        vector.append(cont)
        cont = 0
    
    return vector

def producto_punto(v1, v2):
    res = 0
    for i in range(0, len(v1)):
        res += (v1[i]*v2[i])
    return res

def calcVectorSize(vector):
    sizeV = 0
    for element in vector:
        sizeV += math.pow(element,2)
    return math.sqrt(sizeV)
        
def calcAngulo(v1, v2):
    numerador = producto_punto(v1,v2)
    den1 = calcVectorSize(v1)
    den2 = calcVectorSize(v2)
    res = numerador / (den1 * den2)
    res = math.acos(res)
    return res

def conPalabra(vocabulario):
    diccionario = {}
    total = len(vocabulario)
    for word in set(vocabulario):
        diccionario[word] = [0,0]
    for word in vocabulario:
        diccionario[word][0] += 1
    for word in diccionario:
        diccionario[word][1] = diccionario[word][0] / total  
    
    #sorted_d = sorted(diccionario.items(), key=operator.itemgetter(1))
    
    return diccionario

texto = getCorpus('e960401.htm', 'latin-1')
textoSW = getCorpus('stopwords_es.txt', 'utf-8') 
#vocabulario = sorted(set(texto))
stopwords = cleanTokens3(textoSW)
vocabulario_limpio = cleanTokens3(texto)
print("antes---",len(vocabulario_limpio)) 
vocabulario_limpio = deleteStopWords(vocabulario_limpio, stopwords)
print("despues---",len(vocabulario_limpio))

print("--------------------------------------------------------------------")
con_empresa = getContext(vocabulario_limpio, "empresa")
vector_empresa = createVector(vocabulario_limpio, con_empresa)

print("--------------------------------------------------------------------")
con_agua = getContext(vocabulario_limpio, "agua")
vector_agua = createVector(vocabulario_limpio, con_agua)

print("--------------------------------------------------------------------")
con_compania = getContext(vocabulario_limpio, "compañía")
vector_compania = createVector(vocabulario_limpio, con_compania)


print("--------------------------------------------------------------------")
print("similitud entre agua y empresa:", calcAngulo(vector_agua, vector_empresa))
print("similitud entre empresa y compania:", calcAngulo(vector_empresa, vector_compania))

conteo_palabras = conPalabra(vocabulario_limpio)
print("Palabras mas comunes")
#print(conteo_palabras)
#print(vector_empresa)
