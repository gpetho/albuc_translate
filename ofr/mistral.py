import ollama
import tqdm
import os

# Ensure the directory exists
os.makedirs("mistral", exist_ok=True)

with open("chiralb.txt") as f:
    lines = f.readlines()

model = 'mistral:instruct'

first_prompt = '''The following text is a medieval medical treatise written in Old French, around the 12th-13th centuries.
Try to guess what the text means and translate it line by line into English like this:
Ou cautere de feu comande au malaide qu’il laisse les poilz tant qu’il soient lons et igals; et s’il le poignent a lor nassance, se li estraint les eulz qu’il ne se muevent tant qu’il naissent.
For the fire cautery, instruct the patient to let the hairs grow long and even; and if they prick at their base, hold the eyes steady so they do not move until they grow.
Car en l’ovraige de cest chapistre avient maintes fois evacuation de sanc a l’ovrir la voinne, et a l’incision sus aposteme, et as cures des plaies, et a l’estraction des saiettes, et a l’incision sus la piere, et les semblans choses; ou il a doutance et paor, et en vient li mors a plusors. 
For in the work of this chapter, there is often the evacuation of blood when opening a vein, and incising an abscess, and in the treatment of wounds, and in the extraction of arrows, and in cutting into stones, and similar things; where there is doubt and fear, and many die.
Quant li chiés de l’ajutoire est desaloiez par cause de moistor, et on le remet a leu, et il n’i puet demorer ains revient adés et desalue par petit movement qui avient, si com nos avons esproveit, adonques covient il que tu ramoinnes la dislocation premierement.
When the head of the shoulder is dislocated due to moisture, and it is reset but cannot stay in place, repeatedly dislocating with slight movement as we have experienced, then you must first reset the dislocation.
Here comes the first sentence to translate. Do not add any comments or contextual information about the text, like "Here is the translation", don't provide any comments about the text like, "Wow this is hard!", etc. Do not comment on whether the translation is accurate or not, it doesn't matter. Just translate the text line-by-line into English and that should be the only text produced in the final output file and nothing else:
'''

ctx = 4096

for fnum in range(0, 10):
    with open(f"mistral/mistral_{fnum}.txt", "w") as outfile:
        response = ollama.generate(model=model, prompt=first_prompt + lines[0], options={"num_ctx": ctx})
        print(f"{lines[0].strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)

        for line in tqdm.tqdm(lines[1:]):
            print(len(response['context']))
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
