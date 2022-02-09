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
#generate ppt pdf from latex
from pdflatex import PDFLaTeX

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
section_summary=get_summary(documents, tfidf_results).split('\n')
print("\n--------------------------summarize a section end----------------------------------------\n")
soup_section = TexSoup(section1)
print(soup_section)
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
def add_text_frame(text_list, frame_name, beamer_file):
    """
    add a frame containing itemize texts into a beamer file
    :param text_list: list of text
    :param frame_name: str
    :param beamer_file: file handle
    :return:
    """
    beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
    beamer_file.writelines(r'%' + '\n')
    beamer_file.writelines(r'\begin{itemize}' + '\n')
    for txt in text_list:
        beamer_file.writelines(r'\item' + '\n')
        beamer_file.writelines(txt + '\n')
    beamer_file.writelines(r'\end{itemize}' + '\n')
    beamer_file.writelines(r'\end{frame}' + '\n')
    beamer_file.writelines(r'%' + '\n')

def add_figure_frame(fig_str, frame_name, beamer_file):
    """
    add a frame containing a single figure into a beamer file
    :param fig_str: maybe directly use extracted figure?
    :param frame_name: str
    :param beamer_file: file handle
    :return:
    """

    for fig in fig_str:
        fig_str = str(fig)
        beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
        beamer_file.writelines(r'%' + '\n')
        beamer_file.writelines(fig_str + '\n')
        beamer_file.writelines(r'\end{frame}' + '\n')
        beamer_file.writelines(r'%' + '\n')

with open('presentation_test.tex', 'w') as tex_f:
    # headers and packages
    tex_f.writelines(r'\documentclass{beamer}' + '\n')
    tex_f.writelines(r'\usepackage[T1]{fontenc}' + '\n')
    tex_f.writelines(r'\usepackage[utf8]{inputenc}' + '\n')
    tex_f.writelines(r'\usepackage{lmodern}' + '\n')
    tex_f.writelines(r'\usepackage{textcomp}' + '\n')
    tex_f.writelines(r'\usepackage{lastpage}' + '\n')
    tex_f.writelines(r'%' + '\n')
    tex_f.writelines(r'\title{}'.format('{' + slide_title + '}') + '\n')
    tex_f.writelines(r'%' + '\n')
    tex_f.writelines(r'\begin{document}' + '\n')
    tex_f.writelines(r'\normalsize' + '\n')
    tex_f.writelines(r'\maketitle' + '\n')
    tex_f.writelines(r'%' + '\n')

    add_text_frame(section_summary, 'Introduction', tex_f)

    add_figure_frame(a_sec_figures, 'Introduction', tex_f)

    tex_f.writelines(r'\end{document}' + '\n')



pdfl = PDFLaTeX.from_texfile('presentation_test.tex')
pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
