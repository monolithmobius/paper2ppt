################################################################
#################succeed version###################

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

tx = tx_process = 'AAAI-SenP.1698.tex'

# remove latex comment %
f = open(tx, 'r')
a = f.readlines()
f = open(tx, 'w')
for i in a:
    if i.startswith('%'):
        pass
    else:
        f.write(i)
f.close()

def read_file(path):

    with open(path) as f:
        cntnt = f.read()

    return cntnt

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
# who would use subsubsection and subparagraph anyway...
SUBSEC_ORDERS = (SUBSEC_PATT, SUBSUBSEC_PATT, PARA_PATT, SUBPARA_PATT)
# indicator for removed content by TexSoup
TEXSOUP_CNT_PREFIX = 'mark_removed_content_'
# different latex environment names for different contents to be extracted
LAX_ENV_NAMES = {'figure': ['figure'],
                 'equation': ['equation'],
                 'table': ['table', 'table*']}

#latex text-->pure text, benefit problems of using pure text summarizer, formatting command creates compiled errors so on.
def latex2text(lat_string):
    """
    removing formatting commands in a latex string, thus converting it into a pure text
    :param lat_string:
    :return: string
    """
    return LatexNodes2Text().latex_to_text(lat_string)

# slice text section
print("\n----------------------slice paper section-----------------------------------------------\n")
sec = ''
sec_list = []
sec_title_list = []
line_n_count1 = 0
line_n_count2 = 0
flag = 0
with open(tx, 'r') as f:
    for line in f.readlines():
        line_n_count1 += 1
f.close()

with open(tx, 'r') as f:
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
###############################################DONE:slice paper into /section pieces and put the tiltle,content of each section into a dictionary###############################################

#slice each /section piece into smaller pieces
def parse_latex(sections):
    """
    parse latex file into different sections/subsections
    generate a dict with section titles as keys, section content as values
    section content is again a dict, contains individual subsections/paragraphs
    :param lat_file: str or path
    :return: dict
    """
    # further parse individual sections
    for pat in SUBSEC_ORDERS:
        better_dict = parse_section(sections, pat)

    return better_dict


def split_text_on_pattern(text, patterns, from_start=True, to_end=True):
    """
    split a text based on patterns. generate N sub texts with to_end=True, and N-1 otherwise
    :param text:
    :param patterns: patterns used to split
    :param from_start: if include the start to first pattern match
    :param to_end: if include the last pattern match till end
    :return: dict, pattern: text
    """
    sections = dict()
    # extract different parts
    secs_idxs = []
    sec_titles = []
    for sec_pat in patterns:
        # PROBLEM: special characters ruin everything again...
        idx = text.find(sec_pat)
        sec_titles.append(sec_pat[sec_pat.find('{')+1:sec_pat.find('}')])
        secs_idxs.append((idx, idx + len(sec_pat)))
    # include content before first subsections if desired and available
    if from_start and secs_idxs[0][0] > 10:
        secs_idxs.insert(0, (0, 0))
        sec_titles.insert(0, 'intro')
    # include all the content till the end if desired
    if to_end:
        secs_idxs.append((len(text) + 1, None))
    # get section contents
    for i in range(len(secs_idxs) - 1):
        sections[sec_titles[i]] = (text[secs_idxs[i][1]+1:secs_idxs[i+1][0]-1])
    sections['titles'] = sec_titles

    return sections

def parse_section(sec_content, pattern):
    """
    parse individual sections into different paragraph
    :param sec_content: dict, title: content of each section
    :param pattern: dict, title: content of each section
    :return:
    """
    for title, content in sec_content.items():
        # ignore the titles field
        if title in ('titles', 'article_title'):
            continue

        if content.__class__ is dict:
            # recursion
            sec_content[title] = parse_section(content, pattern)
            continue

        res = re.findall(pattern, content)
        if res:
            # split
            subsecs = split_text_on_pattern(content, res)
            sec_content[title] = subsecs
        else:
            sec_content[title] = content

    return sec_content

better_sec_dict=parse_latex(sec_dict)

#see the dict of slide paper latex into smaller sections:(SUBSEC_PATT, SUBSUBSEC_PATT, PARA_PATT, SUBPARA_PATT) level
#print(better_sec_dict,'\nddddddddddddddddddd\n',better_sec_dict.keys(),'\nddddddddddddddddd\n',better_sec_dict.values(),'\nddddddddddddddd\n')
#for k in better_sec_dict:
    #print(k,':',better_sec_dict[k],'\n',better_sec_dict.__class__)
    #print('\nssssssssssssssssssssssssssssssssssssssssssssssssssssssss\n')

######################################################################DONE:sliced main latex into the smaller sections########################################################################

#summarize text content
bert_sum = Summarizer()
def bert_textsummary(final_section_dict, model=bert_sum, lowest_level=True,
                     num_sentences=1):
    """
    text summarization with bert-extractive-summarizer nlp component
    :param final_section_dict: dict, individual final sectional results from separate_natural_paragraph
    :param model: callable, which model in the transformers package to use
    :param lowest_level: if summarize on lowest level, i.e. natural paragraphs
    :param num_sentences: Number of sentences to use in summarized text
    :return: list of string, one for each natural paragraph if lowest_level is set to True, or a single entry
    """
    # get the text from the dict, and perform summarization on each paragraph of the text
    paras_clean = final_section_dict['text']

    paras_sum = []
    if lowest_level:
        # summarize each paragraph
        for para in paras_clean:
            if para:
                res = model(para, num_sentences=num_sentences)
                paras_sum.append(res)
    else:
        # summarize entire text
        documents = ' '.join(paras_clean)
        try:
            res = model(documents, )
            paras_sum.append(res)
        except ValueError:
            pass

    return paras_sum

def extract_latex_content(lat_string, cnt=('figure', 'table', 'equation')):
    """
    extract equations, figures and tables from a latex string
    this function should be applied `after` separating natural paragraphs
    :param lat_string:
    :param cnt: contents to extract, iterable
    :return: dict
    """
    res = {}
    # convert to TexSoup
    lat_repr = TexSoup(lat_string)
    for cnt_type in cnt:
        count = 0
        all_items = []
        for cnt_name in LAX_ENV_NAMES[cnt_type]:
            items = lat_repr.find_all(cnt_name)
            # remove found items, so only pure text remains
            # I also want to remove the line, so separating natural paragraphs is easier
            for item in items:
                print('\n5555555555555555555555555555555555555555555555555\n', item, item.__class__,'\n5555555555555555555555555555555555555555555555555555555555555555\n')
                lat_repr.replace(item, TEXSOUP_CNT_PREFIX + cnt_type + '_' + str(count))
                count += 1
            all_items.extend(items)
        res[cnt_type] = all_items
    res['text'] = str(lat_repr)
    return res

def separate_natural_paragraph(lax_dict):
    """
    break the latex string into natural paragraphs, and extract the content of it
    natural paragraphs are separated by a blank line in latex
    :param lax_dict: dict returned by extract_lax_content
    :return: list of paragraphs; position of equations, in form of (equation_number, paragraph)
    """
    # identify natural paragraph pattern
    lax_lines = lax_dict['text'].splitlines()
    lax_clean = ''
    para_count = 0
    eqs_map = []
    for line in lax_lines:
        if line.startswith('%'):
            continue
        if line == '':
            # this marks a start of a natural paragraph
            lax_clean = lax_clean + '\n'
            para_count += 1
        elif line.startswith(TEXSOUP_CNT_PREFIX + 'equation'):
            # problem: replace hard coding
            # record the equation is in which paragraph
            # I can safely ignore figures and tables in this case
            eqs_map.append((int(line[line.rfind('_') + 1:]), para_count))
        else:
            # here I want to replace the \n at the end of the line with a space
            lax_clean = lax_clean + line + ' '

    # now I can simply break at \n to get different natural paragraphs
    paras = lax_clean.splitlines()
    count = 0
    paras_final = []
    for para in paras:
        if para in ('', ' '):
            # remove empty lines
            continue
        else:
            # remove latex commands
            para = latex2text(para)
            # now remove the label used to indicated extracted contents
            res_text = ''
            for line in para.splitlines():
                if not line.startswith(TEXSOUP_CNT_PREFIX):
                    # this will combine artificial line breaks created by latex2text
                    res_text += line + ' '

            paras_final.append(res_text)
            count += 1

    return paras_final, eqs_map

def summarize_all_secs(lat_secs_dict, summarizer=bert_textsummary, params={}):
    """
    extract figures, tables and equations from final sections, and perform text summarization
    :param lat_secs_dict: dict of sections, output from parse_latex
    :param summarizer: callable, used to perform summarization
    :param params: dict of keywords arguments, summarizer parameters
    :return: dict
    """
    result = dict()
    for sec_name, sec_cnt in lat_secs_dict.items():
        if sec_name in ('titles', 'article_title'):
            result[sec_name] = sec_cnt
        elif sec_cnt.__class__ == dict:
            # recursion
            result[sec_name] = summarize_all_secs(sec_cnt, summarizer, params)
        elif sec_cnt.__class__ == str:
            sec_cnt_ext = extract_latex_content(sec_cnt)
            sec_cnt_ext['text'], sec_cnt_ext['eqs_pos'] = separate_natural_paragraph(sec_cnt_ext)
            sec_cnt_ext['text_sum'] = summarizer(sec_cnt_ext, **{})
            result[sec_name] = sec_cnt_ext
    return result



decomposed_paper_dict=summarize_all_secs(better_sec_dict)
for k in decomposed_paper_dict:
    print('\n',k,':\n',decomposed_paper_dict[k],'\n')
#######################################################DONE:retrieved differenct type of information for sliced sections ,
################################with a special case of text that summarized with NLP engineering components: https://pypi.org/project/bert-extractive-summarizer/,
#################################the smallest decomposition unit is natural paragraph for text, /paragraph for figure, equation and table,
#equation is in natural paragraph so its first relevant natural paragraph is summarized and attached to it while doing formatting, so its position is marked for later formatting############################################################



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
    # PROBLEM: type checking for fig_str
    fig_str = str(fig_str)
    beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
    beamer_file.writelines(r'%' + '\n')
    beamer_file.writelines(fig_str + '\n')
    beamer_file.writelines(r'\end{frame}' + '\n')
    beamer_file.writelines(r'%' + '\n')


def add_table_frame(table_str, frame_name, beamer_file):
    """
    add a frame containing a table into a beamer file
    :param table_str: maybe directly use extracted table?
    :param frame_name: str
    :param beamer_file: file handle
    :return:
    """
    # PROBLEM: tables are very hard to put in a slide. need to think of a good way
    # PROBLEM: type checking for table_str
    # PROBLEM: use adjustbox package
    table_str = str(table_str)
    beamer_file.writelines(r'\begin{}'.format('{frame}' + '{' + frame_name + '}') + '\n')
    beamer_file.writelines(r'%' + '\n')
    beamer_file.writelines(table_str + '\n')
    beamer_file.writelines(r'\end{frame}' + '\n')
    beamer_file.writelines(r'%' + '\n')


def write_beamer_section(sec_dict, sec_name, f_handle):
    """
    write a section of the summarized result into a beamer file
    :param sec_dict: dict, a section of the result returned by text summarization function
    :param sec_name: str, name of the section, to be used as frame title
    :param f_handle: file handle, beamer file to be generated
    :return:
    """
    # use the same recursive structure as summarize_all_secs
    if 'titles' in sec_dict.keys():
        # recursion
        for tl in sec_dict['titles']:
            write_beamer_section(sec_dict[tl], tl, f_handle)
    else:
        # first write text/equation frames
        # break the text based on equations, if there is any
        if sec_dict['equation']:
            # check which equation(s) belong to which paragraph
            eqs_pos_para = [pos[1] for pos in sec_dict['eqs_pos']]
            uni_eqs_para = sorted(set(eqs_pos_para))
            # break the text into different part on equations, and insert corresponding equations into it
            current_para = 0
            current_uni_eqs = 0
            final_text = []
            txt_f = []
            for txt_sum in sec_dict['text_sum']:
                txt_f.append(txt_sum)
                if current_para in uni_eqs_para:
                    uni_eqs_idx = uni_eqs_para.index(current_para)
                    # there are equations in current paragraph
                    eqs_idx = [i for i in eqs_pos_para if i == uni_eqs_idx]
                    for eq_i in eqs_idx:
                        # add equation into the text
                        txt_f.append(str(sec_dict['equation'][eq_i]))
                    # add a copy current txt_f to final_text
                    final_text.append(txt_f.copy())
                    # reset txt_f to empty, so starting the next frame
                    txt_f = []
        else:
            final_text = [sec_dict['text_sum']]

        # write text frames
        for txt in final_text:
            add_text_frame(txt, sec_name, f_handle)

        # then add figure frames, if any
        # one frame for each figure
        if sec_dict['figure']:
            for fig in sec_dict['figure']:
                add_figure_frame(fig, sec_name, f_handle)

        # table frames, if any
        if sec_dict['table']:
            for tb in sec_dict['table']:
                add_table_frame(tb, sec_name, f_handle)

def generate_beamer(summarized_dict, fname):
    """
    generate beamer and pdf slides from summarized result
    :param summarized_dict: obtained from summarize_all_secs
    :param fname: str or path
    :return:
    """
    # steps
    # create file for writing
    with open(fname, 'w', encoding='utf-8') as fh:
        # write preamble
        fh.writelines(r'\documentclass{beamer}' + '\n')
        fh.writelines(r'\usepackage[T1]{fontenc}' + '\n')
        fh.writelines(r'\usepackage[utf8]{inputenc}' + '\n')
        fh.writelines(r'\usepackage{lmodern}' + '\n')
        fh.writelines(r'\usepackage{textcomp}' + '\n')
        fh.writelines(r'\usepackage{lastpage}' + '\n')
        fh.writelines(r'%' + '\n')

        # write title frame
        fh.writelines(r'\title{}'.format('{' + summarized_dict['article_title'] + '}') + '\n')
        fh.writelines(r'%' + '\n')
        fh.writelines(r'\begin{document}' + '\n')
        fh.writelines(r'\normalsize' + '\n')
        fh.writelines(r'\maketitle' + '\n')
        fh.writelines(r'%' + '\n')

        # start working on individual sections
        secs_list = summarized_dict['titles']
        for sec_name in secs_list:
            sec_cnt = summarized_dict[sec_name]
            # go through each element of summarized_dict in the order of the titles, write frames accordingly
            write_beamer_section(sec_cnt, sec_name, fh)

        # write document end line
        fh.writelines(r'\end{document}' + '\n')

ppt_beamer_file = 'ppt.tex'
generate_beamer(decomposed_paper_dict, ppt_beamer_file)
###################################################################DONE:paper ppt writed##########################################################################################################