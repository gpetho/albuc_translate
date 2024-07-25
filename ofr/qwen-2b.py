import ollama
import tqdm
import os

# Ensure the directory exists
os.makedirs("qwen2", exist_ok=True)

with open("chiralb.txt") as f:
    lines = f.readlines()

model = 'qwen2:7b'

first_prompt = '''The following text is a medieval medical treatise written in Old French, around the 12th-13th centuries.
Try to guess what the text means and translate it line by line into English like this:
Ou cautere de feu comande au malaide qu’il laisse les poilz tant qu’il soient lons et igals; et s’il le poignent a lor nassance, se li estraint les eulz qu’il ne se muevent tant qu’il naissent.
For the fire cautery, instruct the patient to let the hairs grow long and even; and if they prick at their base, hold the eyes steady so they do not move until they grow.
Here comes the first sentence to translate. Do not add any comments or contextual information about the text, like "Here is the translation", don't provide any comments about the text like, "Wow this is hard!", etc. Do not comment on whether the translation is accurate or not, it doesn't matter. Just translate the text line-by-line into English and that should be the only text produced in the final output file and nothing else:
'''

ctx = 4096

for fnum in range(0, 10):
    with open(f"qwen2/qwen2_7b_{fnum}.txt", "w") as outfile:
        response = ollama.generate(model=model, prompt=first_prompt + lines[0], options={"num_ctx": ctx})
        print(f"{lines[0].strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)

        for line in tqdm.tqdm(lines[1:]):
            if len(response['context']) > 3200:
                response = ollama.generate(model=model, prompt=first_prompt + line, options={"num_ctx": ctx})
            else:
                response = ollama.generate(model=model, prompt=line, options={"num_ctx": ctx}, context=response['context'])
            if response['response'].strip() == "" or 'context' not in response:
                response = ollama.generate(model=model, prompt=first_prompt + line, options={"num_ctx": ctx})
            if response['response'].strip() == "":
                print(f"{line.strip()}\t", file=outfile)
            else:
                print(f"{line.strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)
