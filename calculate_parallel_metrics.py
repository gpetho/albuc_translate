'''
Calculate NIST translation quality metric for the document
received on stdin compared to the reference document
provided on the command line using NLTK'c courpus_nist function.
Write the results in a json file which is provided as the second
command line argument.
This json document might contain a list of other scores as well.
The NIST score will be added as a new item to the list.
'''

import sys
import json
import nltk
import nltk.translate.nist_score
import evaluate

# Download the Punkt tokenizer for tokenizing the input
# on the first run.
# nltk.download('punkt')


def main():
    if len(sys.argv) != 3:
        print('Usage: calculate_quality_metrics.py <reference> <output.json>',
              file=sys.stderr)
        sys.exit(1)

    reference = sys.argv[1]

    with open(reference) as ref_file:
        ref_lines = ref_file.readlines()

    cand_lines = sys.stdin.readlines()

    assert len(ref_lines) == len(cand_lines), f'{len(ref_lines)} != {len(cand_lines)}'

    ref_lines = [line.strip() for line in ref_lines]
    cand_lines = [line.strip() for line in cand_lines]

    # NLTK expects the input to be tokenized and each reference
    # to be a *list* of tokenized sentences.
    ref_lines_tokenized = [[nltk.word_tokenize(line,
                                               preserve_line=True)]
                           for line in ref_lines]
    cand_lines_tokenized = [nltk.word_tokenize(line,
                                               preserve_line=True)
                            for line in cand_lines]

    with open(sys.argv[2]) as json_file:
        data = json.load(json_file)

    names = [item['name'] for item in data]

    if 'NIST' not in names:
        score = nltk.translate.nist_score.corpus_nist(ref_lines_tokenized,
                                                      cand_lines_tokenized)

        data.append({'name': 'NIST',
                     'score': score,
                     'implementation': 'nltk.translate.nist_score.corpus_nist',
                     'tok': 'nltk.word_tokenize',
                     'tok_preserve_line': "yes",
                     'version': "3.8.1",
                     })

    if 'METEOR' not in names:
        meteor = evaluate.load('meteor')
        meteor_score = meteor.compute(predictions=cand_lines,
                                      references=ref_lines)

        data.append({'name': 'METEOR',
                     'score': meteor_score['meteor'],
                     'implementation': 'evaluate',
                     'version': "0.4.1",
                     })

    if 'rouge1' not in names or 'rouge2' not in names or 'rougeL' not in names:
        rouge = evaluate.load('rouge')
        rouge_score = rouge.compute(
            predictions=[" ".join(cand_line)
                         for cand_line in cand_lines_tokenized],
            references=[" ".join(ref_line[0])
                        for ref_line in ref_lines_tokenized])

        data.append({'name': 'rouge1',
                     'score': rouge_score['rouge1'],
                     'implementation': 'evaluate',
                     'version': "0.4.1",
                     'use_aggregator': 'True',
                     'use_stemmer': 'True',
                     })

        data.append({'name': 'rouge2',
                     'score': rouge_score['rouge2'],
                     'implementation': 'evaluate',
                     'version': "0.4.1",
                     'use_aggregator': 'True',
                     'use_stemmer': 'True',
                     })

        data.append({'name': 'rougeL',
                     'score': rouge_score['rougeL'],
                     'implementation': 'evaluate',
                     'version': "0.4.1",
                     'use_aggregator': 'True',
                     'use_stemmer': 'True',
                     })

    with open(sys.argv[2], 'w') as json_file:
        json.dump(data, json_file)


if __name__ == '__main__':
    main()
