from xml.dom import minidom
from bs4 import BeautifulSoup
def getRankXML(rawXML, nameXML):
    try:
        xml = minidom.parseString(rawXML)
        review = xml.getElementsByTagName('review')
        return review[0].attributes['rank'].value
    except Exception as e:
        #print("Lectura fallida en", nameXML, "--", e)
        return 0
    
def getLemmas(text):
    lemmas = []
    lines = text.split("\n")
    for line in lines:
        try:
            #print((line.split(" "))[1])
            lemmas.append( (line.split(" "))[1] )
        except:
            continue
    return lemmas

def getTemcorpus(NameDoc, encode):
    
    try:
        f=open(NameDoc, encoding=encode)
        t=f.read()
        f.close()
        if("xml" in NameDoc):
            t = t.replace('&', '')
        return t
    except Exception as e:
        #print("Corpus:",NameDoc,"-", e)
        return False

def getSentimentalDictionary():
    dict1 = {}
    xml = open('senticon.es.xml', encoding='utf-8')
    contents = xml.read()
    soup = BeautifulSoup(contents,'lxml')
    sentimientos = soup.find_all('lemma')
    for i in range(0, len(sentimientos)):
        dict1[sentimientos[i].text[1:-1]] = sentimientos[i].get('pol')
    return dict1

def getSent():
    listS = []
    xml = minidom.parse('senticon.es.xml')
    sentimientos = xml.getElementsByTagName('lemma')
    for i in range(0, len(sentimientos)):
        listS.append(sentimientos[i].firstChild.nodeValue)
    return listS


def analizeText(Text, Dict, Keys):
    summ = 0
    for word in Text:
        if word in Keys:
            summ += float(Dict[word])
    return summ


sentimental_dict = getSentimentalDictionary()
text_dict = {}
Sents = list(sentimental_dict.keys())
sumCategories = {
                'cat1': { 'cant':0, 'suma':0},
                'cat2': { 'cant':0, 'suma':0},
                'cat3': { 'cant':0, 'suma':0},
                'cat4': { 'cant':0, 'suma':0},
                'cat5': { 'cant':0, 'suma':0},
                }
for i in range(2,4280):  #4280
    path1 = 'corpus/' + str(i) + '.xml'
    path2 = 'corpus/' + str(i) + '.review.pos'
    
    rawXML = getTemcorpus(path1,'latin-1')
    rawText = getTemcorpus(path2,'latin-1')
    
    if rawXML == False or rawText == False:
        continue
    textRev = getLemmas(rawText)
    text_dict[str(i)] = {
                        'cat':getRankXML(rawXML,path1), 
                        'sum':analizeText(textRev, sentimental_dict, Sents)
                        }
    print(i)
    



for key in text_dict:
    if text_dict[key]['cat'] == 0:
        continue
    cat = 'cat' + str(text_dict[key]['cat'])
    sumCategories[cat]['cant'] += 1
    sumCategories[cat]['suma'] += text_dict[key]['sum']

print(sumCategories)
