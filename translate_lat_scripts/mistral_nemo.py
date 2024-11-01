
import ollama
import tqdm
import sys
from transformers import AutoTokenizer

with open("lat/all_text.txt") as f:
    lines = f.readlines()

MAX_CTX = 1000
MAX_ATTEMPTS = 3    

model = 'mistral-nemo'
hf_model = "mistralai/Mistral-Nemo-Instruct-2407"
tokenizer = AutoTokenizer.from_pretrained(hf_model)

first_prompt = ('This is from a medieval Latin translation '
                'of the 10th century Arabic textbook on surgery by Albucasis. '
                'Translate into English, do NOT add any notes or comments, '
                'do NOT change to all caps, just print the translation:\n')


def print_context(response):
    print("Context:", len(response['context']), file=sys.stderr)
    print(tokenizer.decode(response['context']))
    print()


def print_response(response, outfile):
    print(response['response'].strip('"'), file=outfile)
    print()
    print_context(response)


for fnum in range(0, 5):
    with open(f"mistral_nemo_{fnum}.txt", "w") as outfile:
        context = []
        for line in tqdm.tqdm(lines):
            attempt = 0
            while True:
                if context:
                    if len(context) < MAX_CTX:
                        print("case a")
                        response = ollama.generate(model=model,
                                                   prompt=line,
                                                   context=context)
                    else:
                        print("case b")
                        decoded_context = tokenizer.decode(response['context'])
                        ctx_splits = decoded_context.split('[INST]')
                        shortened_context = '[INST]' + ctx_splits[1] + '[INST]' + ctx_splits[-1]
                        print(f'{shortened_context=}', file=sys.stderr)
                        context = tokenizer.encode(shortened_context)
                        print(f"{context=}", file=sys.stderr)
                        response = ollama.generate(model=model,
                                                   prompt=line,
                                                   context=context)
                else:
                    print("case c")
                    response = ollama.generate(model=model,
                                               prompt=first_prompt + line)
                if '\n' in response['response']:
                    if attempt < MAX_ATTEMPTS:
                        attempt += 1
                        print_context(response)
                        print(f"Retrying... {attempt}", file=sys.stderr)
                else:
                    break

            if '\n' in response['response']:
                print(response['response'].split('\n')[0].strip('"'),
                      file=outfile)
                context = []
            else:
                print_response(response, outfile)
                context = response.get('context', [])
