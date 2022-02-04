################################################################
#################whatever experiment area###################

#unzip
import zipfile
#latex parser
from TexSoup import TexSoup

    #latex parser to extract string of image name from tex
from TexSoup.category import categorize
from TexSoup.tokens import tokenize
from TexSoup.reader import read_item

#latex generator
from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import italic, NoEscape
#text summarization
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import warnings
from nltk.corpus import stopwords

nltk.download('stopwords')

HANDICAP = 0.85

#extract paper latex from zip
zip = "Bias_Final.zip"
z = zipfile.ZipFile(zip, "r")
z.extractall()
z.close()

#remove latex comment
tx = tx_process = 'AAAI-SenP.1698.tex'
f = open(tx,'r')
a = f.readlines()
f = open(tx,'w')
for i in a:
    if i.startswith('%'):
        pass
    else:
        f.write(i)
f.close()

#make TexSoup object to do parsing
with open(tx_process) as f:
    soup = TexSoup(f)

#retrieve paper title
slide_title = soup.title[0]
print("--------------------------------title latex-----------------------\n")
print(slide_title)
print("--------------------------------title latex end-----------------------\n")


#retrieve paper figures
figures_tex_list = soup.find_all('figure')
print("--------------------------------figure latex-----------------------\n")
print(figures_tex_list)
print("--------------------------------figure latex end-----------------------\n")



print("--------------------------------figure name-----------------------\n")
def read_item_from(string, skip=2):
    buf = tokenize(categorize(string))
    _ = buf.forward(skip)
    return read_item(buf)
i = 0
for img in figures_tex_list:
    item_image = read_item_from(str(img.includegraphics))
    print("\n item image:",img)
    image = item_image[-1]
    image = image.contents[0]
    print("\n image:",image)
print("--------------------------------figure name end-----------------------\n")


#retrieve paper tables
tables_tex_list = soup.find_all('table')
print("\n--------------------------------table latex-----------------------\n")
print(tables_tex_list)
print("\n--------------------------------table latex end-----------------------\n")

#retrieve paper equations
equations_tex_list = soup.find_all('equation')
print("\n--------------------------------equation latex-----------------------\n")
print(equations_tex_list)
print("\n--------------------------------equation latex end-----------------------\n")

#retrieve paper sections
sections_tex_list = soup.find_all('section')
print("\n--------------------------------section latex-----------------------\n")
print(sections_tex_list)
print("\n--------------------------------section latex end-----------------------\n")

#retrieve paper sections
paragraphs_tex_list = soup.find_all('paragraph')
print("\n--------------------------------paragraph latex-----------------------\n")
print(paragraphs_tex_list)
print("\n--------------------------------paragraph latex end-----------------------\n")

#slide paper section
print("\n--------------------------slide paper section-----------------------------------------------\n")
sec1 = sections_tex_list[0]
sec2 = sections_tex_list[1]
print(sec1,sec2)
sec = ''
sec_list = []
flag = False
with open('AAAI-SenP.1698.tex','r') as f:
   # content = f.read()
    for line in f.readlines():
    #    print("linennnnnnnnnnnnnnnnnnnnnnnn")
    #    print(line)
        if line[1:8] == 'section':
            print(line)
            flag = True
        if flag:
           # print(line)
            sec+=line
    print("\nsec\n")
    print(sec)
       # if flag and line[1:8] == 'section':
    print("\nsec\n")

f.close()
print("\n~~~~~~~~~~sec list~~~~~~~~~~~~~~~\n")
print(sec_list)
print("\n~~~~~~~~~~sec list end~~~~~~~~~~~~~~~\n")
print("\n--------------------------slide paper section end-------------------------------------------\n")


#ai text summarization
def remove_punctuation_marks(text):
    punctuation_marks = dict((ord(punctuation_mark), None) for punctuation_mark in string.punctuation)
    return text.translate(punctuation_marks)

def get_lemmatized_tokens(text):
    normalized_tokens = nltk.word_tokenize(remove_punctuation_marks(text.lower()))
    return [nltk.stem.WordNetLemmatizer().lemmatize(normalized_token) for normalized_token in normalized_tokens]

def get_average(values):
    greater_than_zero_count = total = 0
    for value in values:
        if value != 0:
            greater_than_zero_count += 1
            total += value
    return total / greater_than_zero_count

def get_threshold(tfidf_results):
    i = total = 0
    while i < (tfidf_results.shape[0]):
        total += get_average(tfidf_results[i, :].toarray()[0])
        i += 1
    return total / tfidf_results.shape[0]

def get_summary(documents, tfidf_results):
    summary = ""
    i = 0
    while i < (tfidf_results.shape[0]):
        if (get_average(tfidf_results[i, :].toarray()[0])) >= get_threshold(tfidf_results) * HANDICAP:
            summary += ' ' + documents[i]
        i += 1
    return summary

warnings.filterwarnings("ignore")

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print('punkt')
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

text = open('AAAI-SenP.1698.tex', 'r').read()
documents = nltk.sent_tokenize(text)

tfidf_results = TfidfVectorizer(tokenizer=get_lemmatized_tokens,
                                stop_words=stopwords.words('english')).fit_transform(documents)

#paper summary
print("\n--------------------------summary of all---------------------------------------------------\n")
print(get_summary(documents, tfidf_results))
print("\n--------------------------summary end---------------------------------------------------------\n")




