import re
from sys import stdin
from bs4 import BeautifulSoup
import spacy
from sys import stderr

soup = BeautifulSoup(stdin.read(), 'xml')

nlp = spacy.load("xx_ent_wiki_sm")
nlp.add_pipe('sentencizer')

sentence_id = 0
abbrevs =  ['unc.', 'drac.']


for p in soup.body.find_all('p'):
    text = p.get_text()
    # remove ellipses marking unreadable text
    text = re.sub(r'\. \. \. \.', '', text)
    # remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # remove periods surrounding roman numerals if followed by a lower-case letter
    text = re.sub(r' \.([ivxl]+)\. (?=[a-z])', r' \1 ', text)
    text = re.sub(r' \.([ivxl]+)\.(?=[,;])', r' \1', text)
    p_doc = nlp(text)

    # delete current content of p element
    p.clear()
    sent_buffer = ''

    # insert sentences into p element, each sentence is a new <s> element
    for sent in p_doc.sents:
        if sent_buffer:
            if sent.text.lstrip()[0].islower() or sent.text.lstrip()[0] == '.':
                sent_buffer += sent.text + ' '
                continue
            else:
                sentence_id += 1
                s = soup.new_tag('s')
                s['id'] = f"s{sentence_id:04d}"
                s.string = sent_buffer.rstrip()
                p.append(s)
                # add a space after each sentence
                p.append(' ')
                sent_buffer = ''
        for abbrev in abbrevs:
            if sent.text.endswith(abbrev) or sent.text.endswith(abbrev + ','):
                sent_buffer += sent.text + ' '
                print(sent_buffer, file=stderr)
        if sent_buffer:
            continue
        sentence_id += 1
        s = soup.new_tag('s')
        s['id'] = f"s{sentence_id:04d}"
        s.string = sent.text.rstrip()
        p.append(s)
        # add a space after each sentence
        p.append(' ')

    # If the p element ends while the buffer is not empty
    if sent_buffer:
        sentence_id += 1
        s = soup.new_tag('s')
        s['id'] = f"s{sentence_id:04d}"
        s.string = sent_buffer.rstrip()
        p.append(s)
        p.append(' ')


print(str(soup))
