import nltk
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

texto = getCorpus('e960401.htm')
vocabulario = sorted(set(texto))
vocabulario_limpio = cleanTokens1(vocabulario)
vocabulario_eliminado = []
print(vocabulario_limpio)
    
#print(vocabulario[:30])