import sys
import json
import numpy as np
import evaluate

def main():
    if len(sys.argv) != 3:
        print('Usage: calculate_nist.py <reference> <output.json>',
              file=sys.stderr)
        sys.exit(1)

    reference = sys.argv[1]

    with open(reference) as ref_file:
        ref_lines = ref_file.readlines()

    cand_lines = sys.stdin.readlines()

    assert len(ref_lines) == len(cand_lines), f'{len(ref_lines)} != {len(cand_lines)}'

    ref_lines = [line.strip() for line in ref_lines]
    cand_lines = [line.strip() for line in cand_lines]

    with open(sys.argv[2]) as json_file:
        data = json.load(json_file)

    names = [item['name'] for item in data]

    if 'BLEURT' not in names:
        bleurt = evaluate.load('bleurt', 'BLEURT-20')
        bleurt_score = bleurt.compute(predictions=cand_lines,
                                      references=ref_lines)

        data.append({'name': 'BLEURT',
                     'score': float(np.mean(bleurt_score['scores'])),
                     'aggregation': 'mean',
                     'implementation': 'evaluate',
                     'version': "0.4.1",
                     })

        with open(sys.argv[2], 'w') as json_file:
            json.dump(data, json_file)

if __name__ == '__main__':
    main()
