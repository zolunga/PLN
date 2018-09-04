
import nltk
nltk.download()
from nltk.book import *
text5.concordance("great")
text5.concordance("day")
text7.concordance("arms")
text1.concordance("terrible")


text1.similar("terrible")
text2.similar("terrible")
text5.similar("terrible")
text6.similar("terrible") #mas similar


text5.common_contexts(["terrible","sad"])

len(text8) #cantidad de tokens
len(set(text8)) #cantidad de tokens sin repeticion
