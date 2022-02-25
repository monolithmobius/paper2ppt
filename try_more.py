################################################################
#################whatever experiment area###################

#input file path
import os
# unzip
import zipfile
# latex parser
from TexSoup import TexSoup
#regular expression
import re
#comparision
import operator
#convert latex formate text to pure text which has no command and structures.
from pylatexenc.latex2text import LatexNodes2Text
#text summarization with bert-extractive-transformer
from summarizer import Summarizer
import torch



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


def remove_latex_comment(lat_file):
    """
    remove all the comments in a latex file or latex string
    comments include lines starting with '%', as well as latex environments 'comment'
    :param lat_file: file name, path or latex string
    :return: file content as raw string
    """
    if os.path.splitext(lat_file)[-1] == '.tex':
        lat_cnt = read_file(lat_file)
    else:
        lat_cnt = lat_file
    # first remove all the lines start with %
    lat_lines = lat_cnt.splitlines()
    # remove first \n if it is there
    if lat_lines[0] == '\n':
        del lat_lines[0]
    lat_clean = ''
    for line in lat_lines:
        if line.startswith('%'):
            continue
        if line == '':
            # this marks a start of a natural paragraph
            lat_clean = lat_clean + '\n'
        else:
            # should not replace the '\n' with a space at this stage
            # otherwise formatting beamer will be more difficult
            lat_clean = lat_clean + line + '\n'

    # use TexSoup to remove the {comment} section
    lat_repr = TexSoup(lat_clean)
    lat_cmts = lat_repr.find_all('comment')
    for cmt in lat_cmts:
        lat_repr.remove(cmt)

    return str(lat_repr)

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

with open(tx_process) as f:
    soup = TexSoup(f)
# retrieve paper title
slide_title = soup.title[0]
print("--------------------------------retrieve title latex-----------------------\n")
print(slide_title)
print("--------------------------------retrieve title latex end-----------------------\n")

print("\n--------------------------title processing experiment-------------------------------------------\n")
#print(sec_title_list)
title_sample=sec_title_list[0]
#print(title_sample)
cur_brace_index = []
c_index = 0
for c in title_sample:
    if c=='{' or c=='}':
        cur_brace_index.append(c_index)
        print(c)
    c_index+=1
#print(cur_brace_index)
#print(title_sample[cur_brace_index[0]],title_sample[cur_brace_index[1]])
#print(title_sample[cur_brace_index[0]+1:cur_brace_index[1]])

print("\n--------------------------title processing experiment end-------------------------------------------\n")

print("\n--------------------------title processing-------------------------------------------\n")
processed_title_list = []
for title_sample in sec_title_list:
    cur_brace_index = []
    c_index = 0
    for c in title_sample:
        if c == '{' or c == '}':
            cur_brace_index.append(c_index)
        c_index += 1
    processed_title_list.append(title_sample[cur_brace_index[0]+1:cur_brace_index[1]])
print(processed_title_list)
print("\n--------------------------title processing end-------------------------------------------\n")

print("\n--------------------------section processing experiment-------------------------------------------\n")
#print(sec_list)
sec_sample=sec_list[0]
#print(sec_sample)
sec_c_index = 0
for c in sec_sample:
    if c=='}':
        break
    sec_c_index+=1
sec_c_index += 2
sec_sample = sec_sample[sec_c_index:]

test_l = []
test_l.append(sec_sample)
#print(test_l)

print("\n--------------------------section processing experiment end-------------------------------------------\n")

print("\n--------------------------section processing-------------------------------------------\n")
processed_sec_list = []
n_sec = len(sec_list)
n_count_sec = 1
for sec_sample in sec_list:
    sec_c_index = 0
    for c in sec_sample:
        if c == '}':
            break
        sec_c_index += 1
    sec_c_index += 2
    if n_count_sec == n_sec:
        print("\n--------------------------search \document mark-------------------------------------------\n")
        a = re.search(TEX_END_PATT, sec_sample)
        if a:
            b = a.span()
            print(b[0],b[1])
        print("\n--------------------------search \document mark end-------------------------------------------\n")
        sec_sample = sec_sample[sec_c_index:b[0]]
    else:
        sec_sample = sec_sample[sec_c_index:-1]
    sec_sample = remove_latex_comment(sec_sample)
    processed_sec_list.append(sec_sample)
    n_count_sec += 1
print(processed_sec_list)
print("\n--------------------------section processing end-------------------------------------------\n")

print("\n--------------------------put paper sections into dictionary data structure -------------------------------------------\n")
sec_dict = {}
sec_dict['article_title']=slide_title
#print(len(sec_title_list), len(sec_list))
for i in range(len(processed_title_list)):
    sec_dict[processed_title_list[i]] = processed_sec_list[i]
sec_dict['titles']=processed_title_list
print(sec_dict)
for i in sec_dict.items():
    print(i)
print("\n--------------------------put paper sections into dictionary data structure end-------------------------------------------\n")

def read_file(path):

    with open(path) as f:
        cntnt = f.read()

    return cntnt

