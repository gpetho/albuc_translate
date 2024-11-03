import ollama
import tqdm
import os
import logging
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

with open("occ/all_text.txt") as f:
    lines = f.readlines()

MAX_CTX = 1000
MAX_ATTEMPTS = 3

model = 'aya-expanse'
hf_model = "CohereForAI/aya-expanse-8b"
tokenizer = AutoTokenizer.from_pretrained(hf_model)

first_prompt = '''The following text is a medieval medical treatise written in a language that is somwhat similar to Latin, Italian, Spanish and slightly to French as well.
Try to guess what the text means and translate it line by line into English like this:
Quan dolor de juncturas son faytas per humors fregas les quals so enfundutz a quascun membre del cors, lahoras quan veno dolors en los pes, de costuma dels metges es que aquo apelen podragua propriament.
When joint pain is caused by cold humors that infiltrate each part of the body, and pain occurs in the feet, it is customarily called gout by doctors.
E si es necessitat que puntz sia fayt sobre la fassia del pe, lahoras fay am cauteri de punt.
And if it is necessary to make points on the surface of the foot, then do so with a pointed cautery.
E aprop reduzeys le budel o l’atela a la sua conquavitat, e aprop pause la sua ma sobre le loc per so que le budel no yesqua.
Then return the intestine or hernia to its cavity, and place your hand over the area to prevent the intestine from coming out.
E tu ja has ubert entre las coyssas del malaute e dejos lu as pausat un coyssi, et autre servent sia sus las cambas de lu, e autre sus le pietz de lu, le qual tengua las suas mas.
You have already opened the space between the patient's thighs, placed a cushion under them, another servant on their legs, and another on their chest, holding their hands.
Here comes the first sentence to translate. Do not add any comments, like "here is the translation", just reply with the guessed translation and nothing else:
'''


def print_context(response):
    logger.info(f"Context: {str(len(response['context']))}")
    logger.info(tokenizer.decode(response['context']))


def print_response(source, response, outfile):
    print(source.strip() + '\t' + response['response'].strip('"'), file=outfile)
#    print_context(response)

model_fn = model.replace(':', '_')

# Create output directory if it doesn't exist
os.makedirs(f"occ_translations/{model_fn}", exist_ok=True)

for fnum in range(0, 10):
    with open(f"occ_translations/{model_fn.replace(':', '_')}/{model_fn}_{fnum}.txt", "w") as outfile:
        context = []
        for line in tqdm.tqdm(lines):
            attempt = 0
            while True:
                if context and len(context) < MAX_CTX:
                    response = ollama.generate(model=model,
                                                prompt=line,
                                                context=context)
                else:
                    response = ollama.generate(model=model,
                                               prompt=first_prompt + line)
                if '\n' in response['response']:
                    if attempt < MAX_ATTEMPTS:
                        attempt += 1
#                        print_context(response)
                        logger.info(f"Retrying... {attempt}")
                    else:
                        break
                else:
                    break

            if '\n' in response['response']:
                print(line.strip() + '\t' + response['response'].split('\n')[0].strip('"'),
                      file=outfile)
                context = []
            else:
                print_response(line, response, outfile)
                context = response.get('context', [])
