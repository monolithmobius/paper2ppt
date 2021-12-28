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
zip = "Bias_Final.zip"
z = zipfile.ZipFile(zip, "r")
z.extractall()
z.close()

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

with open(tx_process) as f:
    soup = TexSoup(f)

slide_title = soup.title[0]

print("soup figure:",soup.find_all('figure'))
print("\n figures are above \n")
figures_tex_list = soup.find_all('figure')

doc = Document(documentclass="beamer")

doc.preamble.append(Command('title', slide_title))
doc.append(NoEscape(r'\maketitle'))

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
    doc.append("image"+str(i))
    with doc.create(Figure()) as a_graph:
# Figure(position='h!')
#a_graph.add_image(image, width='120px')
        a_graph.add_image(image)
        a_graph.add_caption(image)

doc.generate_tex()
doc.generate_pdf('presentation_neat', clean_tex=False)




