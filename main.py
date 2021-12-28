#unzip
import zipfile
#latex parser
from TexSoup import TexSoup
  #latex parser to do extract string of image name from tex
from TexSoup.category import categorize
from TexSoup.tokens import tokenize
from TexSoup.reader import read_item
#latex generator
from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import italic, NoEscape

#extract the paper latex from zip

'''
append the doc's string
def append_figure(v):
    i=0
    for e in v:
        print("#################################")
        print(e)
        doc.append(r'\frame{')
        doc.append(r'\frametitle{')
        doc.append('figure ' + str(i) + '}')
        doc.append(e)
        doc.append('}')
        i += 1
'''

zip = "Bias_Final.zip"
z = zipfile.ZipFile(zip, "r")
'''{code modification for retrieve images}
#user specify the tex file to extract
tx_process = input("input the tex file name to process:")
tx = z.extract(tx_process)
z.close()
'''
z.extractall()
z.close()
#user specify the tex file to be processed
  #tx = tx_process = input("input the tex file name to process:")
tx = tx_process = 'AAAI-SenP.1698.tex'
#remove comment from latex file
f = open(tx,'r')
a = f.readlines()
f = open(tx,'w')
for i in a:
    if i.startswith('%'):
        pass
    else:
        f.write(i)
f.close()
#open file with latex parser
with open(tx_process) as f:
    soup = TexSoup(f)
#latex parser retrieve paper title
slide_title = soup.title[0]

#latex parser retrive paper images
slide_images = soup.find_all('figure')

first_image = slide_images[0]

print(slide_images)
print(first_image)
image_children = soup.figure.includegraphics
print("test:",image_children)
def read_item_from(string, skip=2):
    buf = tokenize(categorize(string))
    _ = buf.forward(skip)
    return read_item(buf)
item_image = read_item_from(str(image_children))
print(item_image)
image = item_image[-1]
#print(image)
image = image.contents[0]
print(image)

#generate ppt latex
doc = Document(documentclass="beamer")

doc.preamble.append(Command('title', slide_title))
doc.append(NoEscape(r'\maketitle'))

doc.append("this is a title")
#append_figure(image)
with doc.create(Figure(position='h!')) as a_graph:
# Figure(position='h!')
#a_graph.add_image(image, width='120px')
    a_graph.add_image(image)
    a_graph.add_caption('a graph')

doc.append("this is another title")
#append_figure(image)
with doc.create(Figure()) as a_graph:
    a_graph.add_image(image)
    a_graph.add_caption('a graph')
'''''
with doc.create(Section('images')):
    with doc.create(Figure(position='h!')) as a_graph:
        a_graph.add_image(image, width='120px')
        a_graph.add_caption('a graph')
'''

doc.generate_tex()

doc.generate_pdf('presentation', clean_tex=False)
