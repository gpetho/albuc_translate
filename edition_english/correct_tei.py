import re
from bs4 import BeautifulSoup

with open('spink_lewis_TEI.xml') as f:
    soup = BeautifulSoup(f, 'xml')

# iterate over all <div> elements of type "chapter"
for chapter in soup.find_all('div', type='chapter'):
    n = 1
    # iterate over all <div> elements of type "subchapter"
    for subchapter in chapter.find_all('div', type='subchapter'):
        # change the value of the "n" attribute
        subchapter['n'] = str(n)
        n += 1

# iterate over all <p> elements
id = 1
for p in soup.body.find_all('p'):
    # add an "id" attribute
    p['id'] = f'p{id:03}'
    id += 1
    # remove figure references from the text
    p.string = re.sub(r' ?\((as )?figs?\. .+?\)', '', p.get_text())
    # remove footnote numbers
    p.string = re.sub(r'[0-9]', '', p.get_text())
    # in <p> with id p249, remove the figure reference
    if p['id'] == 'p249':
        p.string = re.sub(r' ?\(figs.*', '', p.get_text())
    # delete <p> with id p250 (contained only a figure reference)
    if p['id'] == 'p250':
        p.decompose()

# save the modified XML to a new file
with open('spink_lewis_TEI_modified.xml', 'w') as f:
    f.write(soup.prettify())
