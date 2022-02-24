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

print("\n--------------------------put paper sections into dictionary data structure -------------------------------------------\n")
sec_dict = {}
#print(len(sec_title_list), len(sec_list))
for i in range(len(sec_title_list)):
    sec_dict[sec_title_list[i]] = sec_list[i]
print(sec_dict)
'''
for k, v in zip(sec_title_list, sec_list):
    sec_dict[k] = v
print(sec_dict)
'''
print("\n--------------------------put paper sections into dictionary data structure end-------------------------------------------\n")

# removing formatting commands in a latex string, thus converting it into a pure text
def latex2text(lat_string):
    """
    :param lat_string:
    :return: string
    """
    return LatexNodes2Text().latex_to_text(lat_string)

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

#this is a faild function
def add_table_frame_adjustbox(table_str, frame_name, beamer_file):
    for table in table_str:
        #add usepackage{adjustbox}
        a_table = str(table).split('\n')
        a_table.insert(1, '\\adjustbox{max height=\\textheight, max width=\\textwidth}{')
        a_table.append('}')
        a_table_str = '\n'.join(a_table)
        #add usepackage{adjustbox} end
        beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
        beamer_file.writelines(r'%' + '\n')
        beamer_file.writelines(a_table_str + '\n')
        beamer_file.writelines(r'\end{frame}' + '\n')
        beamer_file.writelines(r'%' + '\n')

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

    print("\n--------------------------see lat_repr---------------------------------------------------\n")
    #print(lat_repr)
    print("\n--------------------------see lat_repr---------------------------------------------------\n")
    for cnt_type in cnt:
        items = lat_repr.find_all(cnt_type)
        # remove found items, so only pure text remains
        for item in items:
            lat_repr.remove(item)
        res[cnt_type] = items
    # also save the pure text
    print("\n--------------------------see res[text]---------------------------------------------------\n")
    res['text'] = str(lat_repr)
 #   res['text'] = res['text'][1:]
    print(res['text'])
    print("\n--------------------------see res[text] end---------------------------------------------------\n")
    return res['text']

def section_level_paper2ppt_auto_generate(list_of_section, title_of_slide):
    # transfer the whole paper latex into ppt beamber latex
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
        tex_f.writelines(r'\title{}'.format('{' + title_of_slide + '}') + '\n')
        tex_f.writelines(r'%' + '\n')
        tex_f.writelines(r'\begin{document}' + '\n')
        tex_f.writelines(r'\normalsize' + '\n')
        tex_f.writelines(r'\maketitle' + '\n')
        tex_f.writelines(r'%' + '\n')

        # section by section
        for section_sample in list_of_section:
            # one section decomposition
            print("\n--------------------------see a section---------------------------------------------------\n")
            print(section_sample)
            print(
                "\n--------------------------see a section end---------------------------------------------------------\n")
            sec_text = extract_text_content(section_sample, cnt=('figure', 'table', 'equation'))
            sec_text = latex2text(sec_text)
            print("\n--------------------------see sec_text--------------------------------------------\n")
            print(sec_text)
            print("\n--------------------------see sec_text end--------------------------------------------\n")
            # use the package Bert-extractive-summarizer
            # this is still extractive, the resulting sentences are still a bit long
            bert_sum = Summarizer()
            sum_res = bert_sum(sec_text, num_sentences=5)
            sum_res = sum_res.splitlines()
            better_sum_res = []
            for i in sum_res:
                if i != '' and i != ' ' and i != '  ' and i != '   ' and i != '    ' and i != '     ' and i != '      ':
                    better_sum_res.append(i)
            better_sum_res = better_sum_res[1:]
            print("\n--------------------------summarize a section----------------------------------------\n")
            print(sum_res)
            print(better_sum_res)
            print("\n--------------------------summarize a section end----------------------------------------\n")
            soup_section = TexSoup(section_sample)
            # print(soup_section)
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

            # one section composition
            add_text_frame(better_sum_res, a_sec_title, tex_f)
            add_figure_frame(a_sec_figures, a_sec_title, tex_f)
            add_table_frame(a_sec_tables, a_sec_title, tex_f)
            add_equation_frame(a_sec_equations, a_sec_title, tex_f)

        tex_f.writelines(r'\end{document}' + '\n')
section_level_paper2ppt_auto_generate(sec_list, slide_title)


print(sec_title_list)

#this is a faild experiment
print("--------------------------------a section table experiment -----------------------\n")
#a_table = str(a_sec_tables[0]).split('\n')
#print(a_table)
#a_table.insert(1,'\\adjustbox{max height=\\textheight, max width=\\textwidth}{')
#a_table.append('}')
#a_table_str = '\n'.join(a_table)
#print("---------------------------------------------------------\n")
#print(a_table_str)
print("--------------------------------a section table experiment end-----------------------\n")






