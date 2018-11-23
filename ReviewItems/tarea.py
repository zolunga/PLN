# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 21:24:07 2018

@author: Alan
"""

from gensim.summarization import summarize
import re
import nltk

def parse_document(doc):
    document = re.sub('\n', ' ', doc)
    document = document.strip()
    sentences = nltk.sent_tokenize(document)
    sentences = [sentence.strip() for sentence in sentences]
    return sentences

def summarize_gensin(text, sumary_ratio=0.1):
    summ = summarize(text, split = True, ratio = sumary_ratio)
    for sentence in summ:
        print (sentence, "\n")
        
        
text = "Adolf Hitlerc (Braunau am Inn, Austria-Hungría, 20 de abril de 1889-Berlín, Alemania, 30 de abril de 1945) fue un político, militar, pintor y escritor alemán, de origen austríaco; canciller imperial desde 1933 y Führer —líder— de Alemania desde 1934 hasta su muerte. Llevó al poder al Partido Nacionalsocialista Obrero Alemán o Partido Nazi,d y lideró un régimen totalitario durante el período conocido como Tercer Reich o Alemania nazi. Además, fue quien dirigió a Alemania durante la Segunda Guerra Mundial, que inició con el propósito principal de cumplir sus planes expansionistas en Europa \
Hitler se afilió al Partido Obrero Alemán, precursor del Partido Nazi, en 1919, y se convirtió en su líder en 1921. En 1923, tras el pronunciamiento en la cervecería Bürgerbräukeller de Múnich, Hitler intentó una insurrección, conocida como el Putsch de Múnich, tras cuyo fracaso fue condenado a cinco años de prisión. Durante su estancia en la cárcel redactó la primera parte de su libro Mi lucha (en alemán, Mein Kampf), en el que expone su ideología junto con elementos autobiográficos.\
Liberado ocho meses después, en 1924, Hitler obtuvo creciente apoyo popular mediante la exaltación del pangermanismo, el antisemitismo y el anticomunismo, sirviéndose de su talento oratorio apoyado por la eficiente propaganda nazi y las concentraciones de masas cargadas de simbolismo.\
Fue nombrado canciller imperial (Reichskanzler) en enero de 1933 y, un año después, a la muerte del presidente Paul von Hindenburg, se autoproclamó líder y canciller imperial (Führer und Reichskanzler), asumiendo así el mando supremo del Estado germano. Transformó la República de Weimar en el Tercer Reich y gobernó con un partido único basado en el totalitarismo y la autocracia de la ideología nazi.\
El objetivo de Hitler era establecer un Nuevo Orden basado en la absoluta hegemonía de la Alemania nazi en el continente europeo. Su política exterior e interior tenía el objetivo de apoderarse de Lebensraum (‘espacio vital’) para los pueblos germánicos. Promovió el rearme de Alemania y tras la invasión de Polonia por la Wehrmacht el 1 de septiembre de 1939, se inició la Segunda Guerra Mundial. Con estos actos, Hitler violó el Tratado de Versalles de 1919, que establecía las condiciones de la paz tras la Primera Guerra Mundial.\
"
texto = parse_document(text)
texto = ' '.join(texto)
summarize_gensin(texto, 0.4)