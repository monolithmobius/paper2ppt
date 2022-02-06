################################################################
#################whatever experiment area###################

# unzip
import zipfile
# latex parser
from TexSoup import TexSoup
# latex parser to extract string of image name from tex
from TexSoup.category import categorize
from TexSoup.tokens import tokenize
from TexSoup.reader import read_item
'''
# latex generator
from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import italic, NoEscape
'''
# text summarization
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import warnings
from nltk.corpus import stopwords

nltk.download('stopwords')

HANDICAP = 0.85

# extract paper latex from zip
zip = "Bias_Final.zip"
z = zipfile.ZipFile(zip, "r")
z.extractall()
z.close()

# remove latex comment
tx = tx_process = 'AAAI-SenP.1698.tex'
f = open(tx, 'r')
a = f.readlines()
f = open(tx, 'w')
for i in a:
    if i.startswith('%'):
        pass
    else:
        f.write(i)
f.close()

# make TexSoup object to do parsing
with open(tx_process) as f:
    soup = TexSoup(f)

# retrieve paper title
slide_title = soup.title[0]
print("--------------------------------retrieve title latex-----------------------\n")
print(slide_title)
print("--------------------------------retrieve title latex end-----------------------\n")

# retrieve paper figures
figures_tex_list = soup.find_all('figure')
print("--------------------------------retrieve figure latex-----------------------\n")
print(figures_tex_list)
print("--------------------------------retrieve figure latex end-----------------------\n")

print("--------------------------------retrieve figure name-----------------------\n")


def read_item_from(string, skip=2):
    buf = tokenize(categorize(string))
    _ = buf.forward(skip)
    return read_item(buf)


i = 0
for img in figures_tex_list:
    item_image = read_item_from(str(img.includegraphics))
    print("\n item image:", img)
    image = item_image[-1]
    image = image.contents[0]
    print("\n image:", image)
print("--------------------------------retrieve figure name end-----------------------\n")

# retrieve paper tables
tables_tex_list = soup.find_all('table')
print("\n--------------------------------retrieve table latex-----------------------\n")
print(tables_tex_list)
print("\n-------------------------------retrieve table latex end-----------------------\n")

# retrieve paper equations
equations_tex_list = soup.find_all('equation')
print("\n--------------------------------retrieve equation latex-----------------------\n")
print(equations_tex_list)
print("\n-----------------------------retrieve equation latex end-----------------------\n")

# retrieve paper paragraph
paragraphs_tex_list = soup.find_all('paragraph')
print("\n--------------------------------retrieve paragraph latex-----------------------\n")
print(paragraphs_tex_list)
print("\n-----------------------------retrieve paragraph latex end-----------------------\n")

# retrieve paper sections
sections_tex_list = soup.find_all('section')
print("\n----------------------------retrieve section latex-----------------------\n")
print(sections_tex_list)
print("\n----------------------------retrieve section latex end-----------------------\n")


# slice text section
print("\n----------------------slice paper section-----------------------------------------------\n")
sec = ''
sec_list = []
sec_title_list = []
line_n_count1 = 0
line_n_count2 = 0
flag = 0
with open('AAAI-SenP.1698.tex', 'r') as f:
    for line in f.readlines():
        line_n_count1 += 1
f.close()

with open('AAAI-SenP.1698.tex', 'r') as f:
    for line in f.readlines():
        line_n_count2 += 1
        if line_n_count2 == line_n_count1:
            sec += line
            sec_list.append(sec)
            break
        if line[1:8] == 'section' and flag == 0:
            sec += line
            sec_title_list.append(line)
            flag = 1
            continue
        if flag == 1:
            if line[1:8] == 'section':
                sec_list.append(sec)
                sec_title_list.append(line)
                sec = ''
            sec += line
f.close()

print('ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\n')
for i in sec_list:
    print(i, '\nssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\n')


print("\n--------------------------slice paper section end-------------------------------------------\n")


# ai text summarization
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

#whole paper summary
print("\n--------------------------summary of all---------------------------------------------------\n")
#print(get_summary(documents, tfidf_results))
print("\n--------------------------summary end---------------------------------------------------------\n")


#one section decomposition
section1 = sec_list[0]
print("\n--------------------------see a section---------------------------------------------------\n")
print(section1)
print("\n--------------------------see a section end---------------------------------------------------------\n")
print("\n--------------------------summarize a section--------------------------------------------\n")
documents = nltk.sent_tokenize(section1)
tfidf_results = TfidfVectorizer(tokenizer=get_lemmatized_tokens,
                                stop_words=stopwords.words('english')).fit_transform(documents)
print(get_summary(documents, tfidf_results))
print("\n--------------------------summarize a section end----------------------------------------\n")
soup_section = TexSoup(section1)
print("--------------------------------retrieve section title-----------------------\n")
a_sec_title= soup_section.section.string
print(a_sec_title)
print("--------------------------------retrieve section title end-----------------------\n")
print("--------------------------------retrieve section figures-----------------------\n")
a_sec_figures = soup_section.find_all('figure')
print(a_sec_figures)
print("--------------------------------retrieve section figures end-----------------------\n")
print("--------------------------------retrieve section tables-----------------------\n")
a_sec_tables = soup_section.find_all('table')
print(a_sec_tables)
print("--------------------------------retrieve section tables end-----------------------\n")

print("--------------------------------retrieve section equations-----------------------\n")
a_sec_equations = soup_section.find_all('equation')
print(a_sec_equations)
print("--------------------------------retrieve section equations end-----------------------\n")
print("--------------------------------slide section paragraphs-----------------------\n")

'''
# slice text section paragraph
print("\n----------------------slice paragraphs of a section-----------------------------------------------\n")
para = ''
sec_para = []
sec_para_title_list = []
sec_line_n_count1 = len(section1.splitlines())
sec_line_n_count2 = 0
para_flag = 0


for line in section1.splitlines():
    print(line)
    sec_line_n_count2 += 1
    if sec_line_n_count2 == sec_line_n_count1:
        para += line
        sec_para.append(para)
        break
    if line[1:10] == 'paragraph' and para_flag == 0:
        para += line
        sec_para_title_list.append(line)
        para_flag = 1
        continue
    if flag == 1:
        if line[1:10] == 'paragraph':
            sec_para.append(para)
            sec_para_title_list.append(para)
            para = ''
        para += line

print('\nppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp\n')
for i in sec_para:
    print(i, '\nppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp\n')
print("\n--------------------------------slide section paragraphs end-----------------------\n")
'''