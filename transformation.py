################################################################
#################on the way new product###################


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

doc = Document(documentclass="beamer")

doc.preamble.append(Command('title', slide_title))
doc.append(NoEscape(r'\maketitle'))
#retrieve paper figures
def read_item_from(string, skip=2):
    buf = tokenize(categorize(string))
    _ = buf.forward(skip)
    return read_item(buf)

figures_tex_list = soup.find_all('figure')

i = 0
for img in figures_tex_list:
    item_image = read_item_from(str(img.includegraphics))
    print("\n item image:",img)
    image = item_image[-1]
    image = image.contents[0]
    print("\n image:",image)
    doc.append("image"+str(i))
    with doc.create(Figure()) as a_graph:
        a_graph.add_image(image)
        a_graph.add_caption(image)

'''
#retrieve paper table
tables_tex_list = soup.find_all('table')
print(tables_tex_list)
'''

'''
i = 0
for img in tables_tex_list:
    item_image = read_item_from(str(img.includegraphics))
    print("\n item image:",img)
    image = item_image[-1]
    image = image.contents[0]
    print("\n image:",image)
    doc.append("image"+str(i))
    with doc.create(Figure()) as a_graph:
        a_graph.add_image(image)
        a_graph.add_caption(image)
'''

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

print("\n-----------------------------------------------------------------------------------\n")
print(get_summary(documents, tfidf_results))
print("\n-----------------------------------------------------------------------------------\n")

#generate latex
doc.generate_tex()
doc.generate_pdf('presentation_neat', clean_tex=False)


