from bs4 import BeautifulSoup
import re

soup = {}

fnames = {'eng': [], 'occ': []}

eng_stopwords = set(['the', 'of', 'and', 'it', 'to', 'in', 'a', 'with', 'is',
                     'then', 'be', 'if', 'that', 'on', 'for', 'as', 'this',
                     'from', 'are', 'by', 'which', 'an', 'at', 's'])
occ_stopwords = set(['e', 'de', 'la', 'que', 'es', 'le', 'en', 'am', 'lu',
                     'sia', 'del', 'aprop', 'a', 'no', 'si', 'lahoras', 'las',
                     'per', 'aquel', 'aquo', 'aquela', 'qual', 'so', 'segon',
                     'les', 'al', 'quan', 'cum', 'dels'])


def normalize(text, lang='eng'):
    '''
    Insert spaces around punctuation marks.
    Lowercase the text.
    '''
    return text
    if lang == 'eng':
        stopwords = eng_stopwords
    else:
        stopwords = occ_stopwords
    punctuation = "-—'.,;:?!()[]’"
    for p in punctuation:
        # text = text.replace(p, f' {p} ')
        text = text.replace(p, f' ')
    text = text.lower()
    # new_text = ''
    # for w in text.split():
    #     if w not in stopwords:
    #         new_text += w + ' '
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing spaces
    text = text.strip()
    return text


with open("AlbucE_sentences.xml") as occ:
    soup['occ'] = BeautifulSoup(occ, "xml")

with open("spink_lewis_sentences.xml") as occ:
    soup['eng'] = BeautifulSoup(occ, "xml")


for lang in ['occ', 'eng']:
    count_lines = 0

    all_text = open(f"{lang}/all_text.txt", "w")
    preface = soup[lang].find('div', {'type': 'preface'})

    fname = f"{lang}/preface.txt"
    fnames[lang].append(fname)
    with (open(fname, "w") as f,
          open(f"lines_{fname}", "w") as f_lines):
        for sentence in preface.find_all('s'):
            print(normalize(sentence.text, lang=lang), file=f)
            print(count_lines, file=f_lines)
            count_lines += 1
            print(normalize(sentence.text, lang=lang), file=all_text)

    for chapter_number in range(1, 4):
        chapter = soup[lang].find('div', {'type': f'chapter', 'n': chapter_number})
        p_children = chapter.find_all('p', recursive=False)

        fname = f"{lang}/chapter-{chapter_number}.txt"
        fnames[lang].append(fname)
        with (open(fname, "w") as f,
              open(f"lines_{fname}", "w") as f_lines):
            for p in p_children:
                for sentence in p.find_all('s'):
                    print(normalize(sentence.text, lang=lang), file=f)
                    print(count_lines, file=f_lines)
                    count_lines += 1
                    print(normalize(sentence.text, lang=lang), file=all_text)

        subchapters = chapter.find_all('div', {'type': f'subchapter'})

        for subchapter in subchapters:
            subchapter_number = subchapter['n']
            subchapter_text = subchapter.text

            fname = f"{lang}/chapter-{chapter_number}-subchapter-{subchapter_number}.txt"
            fnames[lang].append(fname)
            with (open(fname, "w") as f,
                  open(f"lines_{fname}", "w") as f_lines):
                for sentence in subchapter.find_all('s'):
                    print(normalize(sentence.text, lang=lang), file=f)
                    print(count_lines, file=f_lines)
                    count_lines += 1
                    print(normalize(sentence.text, lang=lang), file=all_text)

    all_text.close()

assert len(fnames['eng']) == len(fnames['occ'])

with open("hunalign_batch.txt", 'w') as batch_file:
    for fname_eng, fname_occ in zip(fnames['eng'], fnames['occ']):
        batch_file.write(f"{fname_eng}\t{fname_eng.replace('eng', 'occ')}\t{fname_eng.replace('eng', 'align_out')}\n")
