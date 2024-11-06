import argparse
import re
from pathlib import Path
from bs4 import BeautifulSoup


STOPWORDS = {'eng': set(['the', 'of', 'and', 'it', 'to', 'in', 'a', 'with', 'is',
                         'then', 'be', 'if', 'that', 'on', 'for', 'as', 'this',
                         'from', 'are', 'by', 'which', 'an', 'at', 's']),
             'occ': set(['e', 'de', 'la', 'que', 'es', 'le', 'en', 'am', 'lu',
                         'sia', 'del', 'aprop', 'a', 'no', 'si', 'lahoras', 'las',
                         'per', 'aquel', 'aquo', 'aquela', 'qual', 'so', 'segon',
                         'les', 'al', 'quan', 'cum', 'dels'])}


def normalize(text, lang):
    '''
    Insert spaces around punctuation marks.
    Lowercase the text.
    '''
    return text
    punctuation = "-—'.,;:?!()[]’"
    for p in punctuation:
        # text = text.replace(p, f' {p} ')
        text = text.replace(p, f' ')
    text = text.lower()
    # new_text = ''
    # for w in text.split():
    #     if w not in STOPWORDS[lang]:
    #         new_text += w + ' '
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing spaces
    text = text.strip()
    return text


def main():
    args = parse_args()
    lang = args.language_code
    with open(args.input_file, encoding='utf-8') as xml_file:
        soup = BeautifulSoup(xml_file, "xml")

    # Delete all note elements from soup.
    # Necessary for Arabic XML.
    for note in soup.find_all('note'):
        note.decompose()

    # create lang directory if it doesn't exist
    Path(lang).mkdir(exist_ok=True)

    all_text = open(f"{lang}/all_text.txt", "w", encoding='utf-8')

    preface = soup.find('div', {'type': 'preface'})
    fname = f"{lang}/preface.txt"
    fnames = [fname]
    with open(fname, "w", encoding='utf-8') as f:
        if args.divide_by_sentences:
            for sentence in preface.find_all('s'):
                if args.print_s_tags:
                    # print sentence element in its entirety
                    print(sentence, file=f)
                    print(sentence, file=all_text)
                else:
                    print(normalize(sentence.text, lang=lang), file=f)
                    print(normalize(sentence.text, lang=lang), file=all_text)
        else:
            print(normalize(preface.text, lang=lang), file=f)
            print(normalize(preface.text, lang=lang), file=all_text)

    for chapter_number in range(1, 4):
        chapter = soup.find('div', {'type': 'chapter', 'n': chapter_number})
        p_children = chapter.find_all('p', recursive=False)

        fname = f"{lang}/chapter-{chapter_number}.txt"
        fnames.append(fname)
        with (open(fname, "w", encoding='utf-8') as f):
            for p in p_children:
                if args.divide_by_sentences:
                    for sentence in p.find_all('s'):
                        if args.print_s_tags:
                            print(sentence, file=f)
                            print(sentence, file=all_text)
                        else:
                            print(normalize(sentence.text, lang=lang),
                                  file=f)
                            print(normalize(sentence.text, lang=lang),
                                  file=all_text)
                else:
                    print(normalize(p.text, lang=lang), file=f)
                    print(normalize(p.text, lang=lang), file=all_text)

        subchapters = chapter.find_all('div', {'type': 'subchapter'})

        for subchapter in subchapters:
            subchapter_number = subchapter['n']

            fname = f"{lang}/chapter-{chapter_number}-subchapter-{subchapter_number}.txt"
            fnames.append(fname)
            with open(fname, "w", encoding='utf-8') as f:
                if args.divide_by_sentences:
                    for sentence in subchapter.find_all('s'):
                        if args.print_s_tags:
                            print(sentence, file=f)
                            print(sentence, file=all_text)
                        else:
                            print(normalize(sentence.text, lang=lang),
                                  file=f)
                            print(normalize(sentence.text, lang=lang),
                                  file=all_text)
                else:
                    print(normalize(subchapter.text, lang=lang), file=f)
                    print(normalize(subchapter.text, lang=lang),
                          file=all_text)

    all_text.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Extract text by subchapter')
    parser.add_argument('language_code', type=str,
                        help='3-letter language code')
    parser.add_argument('input_file', type=str,
                        help='Path to input xml file')
    # add boolean argument to specify whether to divide by sentences
    parser.add_argument('-s', '--divide_by_sentences', action='store_true',
                        help='Print each sentence on a new line')
    parser.add_argument('-t', '--print_s_tags', action='store_true',
                        help='Print the s tags')

    return parser.parse_args()


if __name__ == '__main__':
    main()
