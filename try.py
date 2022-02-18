################################################################
#################whatever experiment area###################

# unzip
import zipfile
# latex parser
from TexSoup import TexSoup
#regular expression
import re
#convert latex formate text to pure text which has no command and structures.
from pylatexenc.latex2text import LatexNodes2Text
# text summarization with nltk
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import warnings
from nltk.corpus import stopwords
#generate ppt pdf from latex
from pdflatex import PDFLaTeX

# extract paper latex from zip
zip = "Bias_Final.zip"
z = zipfile.ZipFile(zip, "r")
z.extractall()
z.close()

# remove latex comment %
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

''''' not working remove {comment} section
# use TexSoup to remove the {comment} section
with open(tx_process) as f:
    lat_repr = TexSoup(f)
lat_cmts = lat_repr.find_all('comment')
for cmt in lat_cmts:
    lat_repr.remove(cmt)
f = open(tx, 'w')
f.write(str(lat_repr))
f.close()
'''''

#regular experession with re package
  # detect main text starting pattern
MAIN_TEX_PATT = re.compile(r'(\\begin\s*\{\s*document\s*\})', re.I)
  # detect end pattern
TEX_END_PATT = re.compile(r'(\\end\s*\{\s*document\s*\})', re.I)
  # detect section{}, subsection{}, subsubsection{}, paragraph{}, subparagraph{}
SEC_PATT = re.compile(r'\\section\s*\{[^\n]+?\}', re.I)   # \\->\, \s->any space,[^\n]->no \n,+?->at least one thing existing, \}->}
PARA_PATT = re.compile(r'\\paragraph\s*\{[^\n]+?\}', re.I)
SUBPARA_PATT = re.compile(r'\\subparagraph\s*\{[^\n]+?\}', re.I)
SUBSEC_PATT = re.compile(r'\\subsection\s*\{[^\n]+?\}', re.I)
SUBSUBSEC_PATT = re.compile(r'\\subsubsection\s*\{[^\n]+?\}', re.I)

#store whole paper latex string in paper_latex
paper_latex = open(tx).read()
print("--------------------------------read paper latex-----------------------\n")
#print(paper_latex)
print("--------------------------------read paper latex end-----------------------\n")

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

# removing formatting commands in a latex string, thus converting it into a pure text
def latex2text(lat_string):
    """
    :param lat_string:
    :return: string
    """
    return LatexNodes2Text().latex_to_text(lat_string)


# ai text summarization with nltk
nltk.download('stopwords')

HANDICAP = 0.5

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
##### ai text summarization with nltk end #####

#format text content into beamer ppt latex
def add_text_frame(text_list, frame_name, beamer_file):

    beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
    beamer_file.writelines(r'%' + '\n')
    beamer_file.writelines(r'\begin{itemize}' + '\n')
    for txt in text_list:
        beamer_file.writelines(r'\item' + '\n')
        beamer_file.writelines(txt + '\n')
    beamer_file.writelines(r'\end{itemize}' + '\n')
    beamer_file.writelines(r'\end{frame}' + '\n')
    beamer_file.writelines(r'%' + '\n')

#format figure content into beamer ppt latex
def add_figure_frame(fig_str, frame_name, beamer_file):

    for fig in fig_str:
        fig_str = str(fig)
        beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
        beamer_file.writelines(r'%' + '\n')
        beamer_file.writelines(fig_str + '\n')
        beamer_file.writelines(r'\end{frame}' + '\n')
        beamer_file.writelines(r'%' + '\n')

#format table content into beamer ppt latex
def add_table_frame(table_str, frame_name, beamer_file):

    for table in table_str:
        table_str = str(table)
        beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
        beamer_file.writelines(r'%' + '\n')
        beamer_file.writelines(table_str + '\n')
        beamer_file.writelines(r'\end{frame}' + '\n')
        beamer_file.writelines(r'%' + '\n')

#format equation content into beamer ppt latex
def add_equation_frame(equation_str, frame_name, beamer_file):
    for equation in equation_str:
        beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
        beamer_file.writelines(r'%' + '\n')
        equation_str = str(equation)
        beamer_file.writelines(equation_str + '\n')
        beamer_file.writelines(r'\end{frame}' + '\n')
        beamer_file.writelines(r'%' + '\n')


#for a smallest string level section, extract text content latex
def extract_text_content(lat_string, cnt=('figure', 'table', 'equation')):
    """
    :param lat_string:
    :param cnt: contents to extract, iterable
    :return: dict
    """
    res = {}
    # convert to TexSoup
    lat_repr = TexSoup(lat_string)
    for cnt_type in cnt:
        items = lat_repr.find_all(cnt_type)
        # remove found items, so only pure text remains
        for item in items:
            lat_repr.remove(item)
        res[cnt_type] = items
    # also save the pure text
    res['text'] = str(lat_repr)
    return res['text']


#transfer the whole paper latex into ppt beamber latex
with open('presentation_test.tex', 'w') as tex_f:
    # headers and packages
    tex_f.writelines(r'\documentclass{beamer}' + '\n')
    tex_f.writelines(r'\usepackage[T1]{fontenc}' + '\n')
    tex_f.writelines(r'\usepackage[utf8]{inputenc}' + '\n')
    tex_f.writelines(r'\usepackage{lmodern}' + '\n')
    tex_f.writelines(r'\usepackage{textcomp}' + '\n')
    tex_f.writelines(r'\usepackage{lastpage}' + '\n')
    tex_f.writelines(r'\usepackage{adjustbox}' + '\n')
    tex_f.writelines(r'%' + '\n')
    tex_f.writelines(r'\title{}'.format('{' + slide_title + '}') + '\n')
    tex_f.writelines(r'%' + '\n')
    tex_f.writelines(r'\begin{document}' + '\n')
    tex_f.writelines(r'\normalsize' + '\n')
    tex_f.writelines(r'\maketitle' + '\n')
    tex_f.writelines(r'%' + '\n')

    #section by section
    for section_sample in sec_list:
        # one section decomposition
        print("\n--------------------------see a section---------------------------------------------------\n")
        print(section_sample)
        print(
            "\n--------------------------see a section end---------------------------------------------------------\n")
        print("\n--------------------------summarize a section--------------------------------------------\n")
        sec_text = extract_text_content(section_sample, cnt=('figure', 'table', 'equation'))
        sec_text=latex2text(sec_text)
        documents = nltk.sent_tokenize(sec_text)
        tfidf_results = TfidfVectorizer(tokenizer=get_lemmatized_tokens,
                                        stop_words=stopwords.words('english')).fit_transform(documents)
        section_summary = get_summary(documents, tfidf_results).split('\n')
        better_section_summary = []
        print(section_summary)
        for i in section_summary:
            if i != '' and i !=' ' and i != '  ' and i!='   ' and i!='    ' and i!='     ' and i!='      ':
                better_section_summary.append(i)
        for i in better_section_summary:
            print(i)
        print(better_section_summary)
        print("\n--------------------------summarize a section end----------------------------------------\n")
        soup_section = TexSoup(section_sample)
        #print(soup_section)
        print("--------------------------------retrieve section title-----------------------\n")
        a_sec_title = soup_section.section.string
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

        #one section composition
        add_text_frame(better_section_summary, a_sec_title, tex_f)
        add_figure_frame(a_sec_figures, a_sec_title, tex_f)
        add_table_frame(a_sec_tables,a_sec_title,tex_f)
        add_equation_frame(a_sec_equations, a_sec_title, tex_f)

    tex_f.writelines(r'\end{document}' + '\n')

print(sec_title_list)

print("--------------------------------a section table experiment -----------------------\n")
print(a_sec_tables)
print("--------------------------------a section table experiment end-----------------------\n")



#for a smallest string level section, decomposite it into dict,xtract equations, figures and tables from a latex string
def extract_latex_content(lat_string, cnt=('figure', 'table', 'equation')):
    """
    :param lat_string:
    :param cnt: contents to extract, iterable
    :return: dict
    """
    res = {}
    # convert to TexSoup
    lat_repr = TexSoup(lat_string)
    for cnt_type in cnt:
        items = lat_repr.find_all(cnt_type)
        # remove found items, so only pure text remains
        for item in items:
            lat_repr.remove(item)
        res[cnt_type] = items
    # also save the pure text
    res['text'] = str(lat_repr)
    return res




