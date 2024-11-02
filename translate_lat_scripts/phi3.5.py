import ollama
import tqdm
import os
import logging
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

with open("lat/all_text.txt") as f:
    lines = f.readlines()

MAX_CTX = 500
MAX_ATTEMPTS = 3

model = 'phi3.5'
hf_model = "microsoft/Phi-3.5-mini-instruct"
tokenizer = AutoTokenizer.from_pretrained(hf_model)

first_prompt = ('This is from a medieval Latin translation '
                'of the 10th century Arabic textbook on surgery by Albucasis. '
                'Translate into English, do NOT add any notes or comments, '
                'do NOT change to all caps, just print the translation:\n')


def print_context(response):
    logger.info(f"Context: {str(len(response['context']))}")
    logger.info(tokenizer.decode(response['context']))


def print_response(source, response, outfile):
    print(source.strip() + '\t' + response['response'].strip('"'), file=outfile)
#    print_context(response)

# Create output directory if it doesn't exist
os.makedirs(f"lat_translations/{model}", exist_ok=True)

for fnum in range(0, 3):
    with open(f"lat_translations/{model}/{model}_{fnum}.txt", "w") as outfile:
        context = []
        for line in tqdm.tqdm(lines):
            attempt = 0
            while True:
                if context and len(context) < MAX_CTX:
                    # if len(context) < MAX_CTX:
                        response = ollama.generate(model=model,
                                                   prompt=line,
                                                   context=context)
                    # else:
                    #     decoded_context = tokenizer.decode(response['context'])
                    #     ctx_splits = decoded_context.split('<|eot_id|>')
                    #     shortened_context = '<|eot_id|>'.join([ctx_splits[0],
                    #                                            ctx_splits[1],
                    #                                            ctx_splits[2],
                    #                                            ctx_splits[-2],
                    #                                            ctx_splits[-1]])
                    #     shortened_context = shortened_context.replace('<|begin_of_text|>', '')
                    #     shortened_context = shortened_context.replace('Cutting Knowledge Date: December 2023', '')
                    #     logger.info(f'{shortened_context=}')
                    #     context = tokenizer.encode(shortened_context)
                    #     logger.info(f"{context=}")
                    #     response = ollama.generate(model=model,
                    #                                prompt=line,
                    #                                context=context)
                else:
                    response = ollama.generate(model=model,
                                               prompt=first_prompt + line)
                if '\n' in response['response'].strip():
                    if attempt < MAX_ATTEMPTS:
                        attempt += 1
#                        print_context(response)
                        logger.info(f"Retrying... {attempt}")
                    else:
                        break
                else:
                    break

            if '\n' in response['response']:
                print(line.strip() + '\t' + response['response'].strip().split('\n')[0].strip('"'),
                      file=outfile)
                context = []
            else:
                print_response(line, response, outfile)
                context = response.get('context', [])
