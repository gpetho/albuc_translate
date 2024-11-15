'''
Align the original and manually modified XML files.
'''

from bs4 import BeautifulSoup
import spacy
import re
nlp = spacy.load("xx_ent_wiki_sm")
nlp.add_pipe('sentencizer')

with open('ChirAlbT_text_bfm.xml') as f:
    original = f.read()

class SentenceCount():
    def __init__(self):
        self.count = 1

def add_numbering(xml_text):
    xml_text = xml_text.replace('<head>', '<p type="head">')
    xml_text = xml_text.replace('</head>', '</p>')

    soup = BeautifulSoup(xml_text, 'xml')

    # Add successive numbers to p elements
    i = 1
    scount = SentenceCount()

    for p in soup.body.find_all('p'):
        p['n'] = f"p{i:04d}"
        i += 1

        if p.text.strip() == '':
            print('Empty paragraph:', scount.count)
            print(p)
            continue

        for num in p.find_all('num'):
            num_text = num.get_text()
            num_text = num_text.replace('j', 'i')
            num_text = num_text.upper()
            num_text = num_text.replace('.', '')
            num.string = num_text

        p_content = p.decode_contents()

        p_content = p_content.replace('.b.', '<letter>.b.</letter>')
        p_content = p_content.replace('.g.', '<letter>.g.</letter>')
        p_content = p_content.replace('.ie.', '<num>.i<sup>e</sup>.</num>')

        # remove XML comments
        p_content = re.sub(r'\s+<!--.*?-->\s+', ' ', p_content)
        p_content = re.sub(r'\s+', ' ', p_content)

        new_content = ''
        p_doc = nlp(p_content)
        for sent in p_doc.sents:
            # Inelegant solution, but does what is necessary:
            if ('"55ra"' in sent.text    # This would be an <s> element that just contains a <pb> element, no text
                or '"4va"' in sent.text
                or '"11vb"' in sent.text
                or '"15ra"' in sent.text
                or '"15rb"' in sent.text
                or '"15rb"' in sent.text
                or '"27ra"' in sent.text):
                continue

            new_content += f'<s id="s{scount.count:04d}">{sent.text}</s>\n'
            scount.count += 1

        p.clear()               # Clear the current content inside <p>
        p.append(BeautifulSoup(new_content, "html.parser"))  # Insert modified content


#        text = p.get_text()
        # remove ellipses marking unreadable text
    #    text = re.sub(r'\. \. \. \.', '', text)
        # remove extra whitespace
#        text = re.sub(r'\s+', ' ', text)
        # remove periods surrounding drachm symbol and roman numerals
#        text = re.sub(r' \.ʒ\.([ivxlIVXL]+)\.', r' ʒ \1', text)
        # remove periods surrounding roman numerals if followed by a lower-case letter
#        text = re.sub(r' \.([ivxlIVXL]+)\. (?=[a-z])', r' \1 ', text)
#        text = re.sub(r' \.([ivxlIVXL]+)\.(?=[,;])', r' \1', text)
    
    return soup


with open('ChirAlbT_text_bfm_mod.xml', 'w') as f:
    f.write(str(add_numbering(original)))
