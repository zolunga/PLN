import nltk
import math
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader
import re


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

def getCorpus(NameDoc):
    ''' Obtiene los tokens del texto y elimina algunos caracteres'''
    f=open(NameDoc, encoding='latin-1')
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
    '''Solo limpia el vocabulario'''
    vl = []#voc limp
    palabra_limpia = "";
    for word in vocabulario:
        palabra_limpia = ""
        for letter in word:
            if re.match(r'[a-záéíóú]', letter):
                palabra_limpia += letter
        if palabra_limpia != "":
            vl.append(palabra_limpia)
    #print(vl)
    return vl

def getContext(vocabulario, palabra):
    '''
    Recibe el bocabulario completo y la palabra que va a buscar, returna el 
    vector
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
            if vocabulario[x] in list_pal_con[i]:
                cont+=1
        vector.append(cont)
        cont = 0
    
    return vector


def calcVectorSize(vector):
    sizeV = 0
    for element in vector:
        sizeV += math.pow(element,2)
    return math.sqrt(sizeV)
        
def calcAngulo(v1, v2):
    numerador = 0
    for i in range (0, len(v1) ):
        numerador += (v1[i] * v2[i])
        #print(v1[i] * v2[i])
        #print( numerador )
    den1 = calcVectorSize(v1)
    den2 = calcVectorSize(v2)
    #print(numerador)
    #print(den1 * den2)
    return numerador / den1 * den2

texto = getCorpus('e960401.htm')
vocabulario = sorted(set(texto))
vocabulario_limpio = cleanTokens3(texto)
#print(len(vocabulario_limpio))
con_empresa = getContext(vocabulario_limpio, "empresa")
vector_empresa = createVector(vocabulario_limpio, con_empresa)
size_vector_empresa = calcVectorSize(vector_empresa)

con_agua = getContext(vocabulario_limpio, "agua")
vector_agua = createVector(vocabulario_limpio, con_agua)
size_vector_agua = calcVectorSize(vector_agua)

print(calcAngulo(vector_agua, vector_empresa))

#print(vector_empresa)
#print(vector_empresa)
