from sys import argv
from pathlib import Path
import json
import tqdm
import bert_score


input_dir = Path(argv[1])
output_dir = Path(argv[2])

TRUNCATE_CHARACTERS = 4000
MODEL = 'microsoft/deberta-xlarge-mnli'

EXCLUDE_FILES = [
]
reference_file = input_dir / "spink_lewis.ref.txt"
mt_files = [
    input_dir / "chatgpt.mt.txt",
#    input_dir / "claude.mt.txt",
]

trans_dir = Path(input_dir) / 'translations'

# iterate over subdirectories of trans_dir and add
# the files in it with their relative path to mt_files

for subdir in trans_dir.iterdir():
    if subdir.is_dir():
        for file in subdir.iterdir():
            if file.name not in EXCLUDE_FILES:
                mt_files.append(file)

json_files = [str(fname).replace(str(input_dir), str(output_dir)) + '.json'
              for fname in mt_files]

scorer = bert_score.BERTScorer(lang="en", nthreads=12, batch_size=16,
                               model_type=MODEL,
                               rescale_with_baseline=True)

with open(reference_file) as ref_file:
    ref_lines = ref_file.readlines()
    ref_lines = [line.strip() for line in ref_lines]

print(mt_files)

for mt_fname, json_fname in tqdm.tqdm(list(zip(mt_files, json_files))):
    try:
        with open(json_fname) as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                print(f"Error in {json_fname}")
    except FileNotFoundError:
        continue

    names = [item['name'] for item in data]
    if 'BERTScore' in names:
        if data[-1]['model_type'] == MODEL:
            continue
        data = data[:-1]

    print(mt_fname)
    with open(mt_fname) as mt_file:
        mt_lines = mt_file.readlines()
        mt_lines = [line.strip()[:TRUNCATE_CHARACTERS] for line in mt_lines]

        _, _, F1 = scorer.score(mt_lines, ref_lines, verbose=True)

        data.append({'name': 'BERTScore',
                    'score': float(f'{F1.mean():.3f}'),
                    'aggregation': 'mean',
                    'metric': 'F1',
                    'model_type': MODEL,
                    'version': "0.3.13",
                    'rescale_with_baseline': True,
                    'truncate above characters': TRUNCATE_CHARACTERS,
                    })

        with open(json_fname, 'w') as json_file:
            json.dump(data, json_file)
