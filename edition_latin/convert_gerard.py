import re
from bs4 import BeautifulSoup

replacements = {
    'LIB.': 'Liber',
    'DEI.': 'Dei.',
    'Cap.': 'Caput',
    'PRAEFATIO.': 'Praefatio.',
    'ALBVCASIS.': 'Albucasis.',
    'GLORIA.': 'Gloria.',
    ' IN ': ' in ',
    ' VT ': ' ut ',
    'ij': 'ii',
    'ę': 'ae',
    'unc.': 'uncia',
}

with open('Albucasis_Chirurgia_la.xml', encoding='utf-8') as infile:
    doc = infile.read()

# delete facsimile part of the document
doc = re.sub(r'<facsimile[^>]*>.*?</facsimile>', '', doc, flags=re.DOTALL)

for old, new in replacements.items():
    doc = doc.replace(old, new)

# delete label, sic and note elements and their content
doc = re.sub(r'<sic[^>]*>.*?</sic>', '', doc, flags=re.DOTALL)
doc = re.sub(r'<note[^>]*>.*?</note>', '', doc, flags=re.DOTALL)
doc = re.sub(r'<label[^>]*>.*?</label>', '', doc, flags=re.DOTALL)

# remove figure tags
doc = re.sub(r'<figure [^>]*>', '', doc)

# replace lb tags with the break="no" attribute, along with preceding line breaks, whitespace and a possible pb tag, by an empty string
doc = re.sub(r'\s*(<pb[^>]*>\s*)?<lb[^>]*break="no"[^>]*>', '', doc)

# replace lb or pb tags preceded by a hyphen, whitespace and a possible pb tag by an empty string, deleting the hyphen, pb andwhitespace
doc = re.sub(r'(\-\s*(<pb[^>]*>\s*)?<lb[^>]*> ?)', '', doc)

doc = re.sub(r'\s*<lb[^>]*>\s*', ' ', doc)

doc = re.sub(r'\s*<pb[^>]*>\s*', ' ', doc)

# replace <head> tags by paragraph tags
doc = re.sub(r'<head>', '<p type="head">', doc)
doc = re.sub(r'</head>', '</p>', doc)

# remove "hi" opening and closing tags
doc = re.sub(r'<hi [^>]*>', '', doc)
doc = re.sub(r'</hi>', '', doc)

## replace lb or pb tags between other tags by a line break
#doc = re.sub(r'>\s*<[lp]b[^>]*>\s*<', r'>\n<', doc)

# insert a line break before each div tag
doc = re.sub(r'\s*<div', '\n<div', doc)

doc = re.sub(r'\n +', '\n', doc)
doc = re.sub(r'\n+', '\n', doc)

# if a word begins with at least three uppercase letters, and the word is not followed by a dot, change all but the first letter to lowercase
doc = re.sub(r'\b([A-Z]{3,})([a-z]*)\b(?!\.)', lambda m: m.group(1).replace('V', 'u').title() + m.group(2), doc)

with open('Albucasis_Chirurgia_la_converted.xml', 'w', encoding='utf-8') as outfile:
    outfile.write(doc)

# open the converted file with BeautifulSoup
with open('Albucasis_Chirurgia_la_converted.xml', encoding='utf-8') as infile:
    soup = BeautifulSoup(infile, 'xml')

body = soup.body
# find all top-level divs
divs = body.find_all('div', recursive=False)
divs[1].decompose()

# Find all divs with type="part", change the type to "chapter" and add a new attribute "n".
# The first such div should be numbered "1", the second "2", etc.
part_divs = body.find_all('div', type='part')
for i, part_div in enumerate(part_divs, start=1):
    part_div['type'] = 'chapter'
    part_div['n'] = str(i)

# Iterate over all divs with type="chapter".
for ch_num, chapter_div in enumerate(body.find_all('div', type='chapter'), start=1):
    subchapter_divs = chapter_div.find_all('div', recursive=False)
    for i, subchapter_div in enumerate(subchapter_divs, start=0):
        subchapter_div['type'] = 'subchapter'
        if ch_num == 2:
            subchapter_div['n'] = str(i + 1)
        else:
            subchapter_div['n'] = str(i)

# Find all divs with type="subchapter" and n="0".
# Remove the div tags and make the content of the divs children of the parent div before all other children.
for subchapter_div in body.find_all('div', type='subchapter', n='0'):
    children = list(subchapter_div.children)
    next_sibling = subchapter_div.next_sibling
    for child in children:
        print(f"child: '{child}'")
        # insert copy of the child before the next sibling
        next_sibling.insert_before(child)
    # remove the div tag
    subchapter_div.decompose()


# save the modified document
with open('Albucasis_Chirurgia_la_converted.xml', 'w', encoding='utf-8') as outfile:
    outfile.write(str(soup))
