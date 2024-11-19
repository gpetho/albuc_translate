import sys
import os
import json
import numpy as np
import evaluate


def main():
    if len(sys.argv) != 2:
        print('Usage: calculate_gpu_metrics.py <language_code>',
              file=sys.stderr)
        sys.exit(1)

    language_code = sys.argv[1]
    base_dir = f'aligned_sl_{language_code}/translations'
    ref_file_path = f'aligned_sl_{language_code}/spink_lewis.ref.txt'

    with open(ref_file_path) as ref_file:
        ref_lines = ref_file.readlines()
    ref_lines = [line.strip() for line in ref_lines]

    bleurt = evaluate.load('bleurt', 'BLEURT-20')

    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            for mt_file in os.listdir(subdir_path):
                mt_file_path = os.path.join(subdir_path, mt_file)
                with open(mt_file_path) as mt_file_obj:
                    cand_lines = mt_file_obj.readlines()
                print("Working on", mt_file_path)
                cand_lines = [line.strip() for line in cand_lines]

                assert len(ref_lines) == len(cand_lines), f'{len(ref_lines)} != {len(cand_lines)}'

                output_json_path = f'sacrebleu_output_{language_code}/translations/{subdir}/{mt_file}.json'
                with open(output_json_path) as json_file:
                    data = json.load(json_file)

                names = [item['name'] for item in data]

                if 'BLEURT' not in names:
                    bleurt_score = bleurt.compute(predictions=cand_lines,
                                                  references=ref_lines)

                    data.append({'name': 'BLEURT',
                                 'score': float(np.mean(bleurt_score['scores'])),
                                 'aggregation': 'mean',
                                 'implementation': 'evaluate',
                                 'version': "0.4.1",
                                 })

                    with open(output_json_path, 'w') as json_file:
                        json.dump(data, json_file)


if __name__ == '__main__':
    main()