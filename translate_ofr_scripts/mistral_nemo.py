import ollama
import tqdm
import sys

with open("ofr/all_text.txt") as f:
    lines = f.readlines()

model = 'mistral-nemo'

first_prompt = '''The following text is a medieval medical treatise written in Old French, around the 12th-13th centuries.
Try to guess what the text means and translate it line by line into English like this:
Ou cautere de feu comande au malaide qu’il laisse les poilz tant qu’il soient lons et igals; et s’il le poignent a lor nassance, se li estraint les eulz qu’il ne se muevent tant qu’il naissent.
For the fire cautery, instruct the patient to let the hairs grow long and even; and if they prick at their base, hold the eyes steady so they do not move until they grow.
Car en l’ovraige de cest chapistre avient maintes fois evacuation de sanc a l’ovrir la voinne, et a l’incision sus aposteme, et as cures des plaies, et a l’estraction des saiettes, et a l’incision sus la piere, et les semblans choses; ou il a doutance et paor, et en vient li mors a plusors. 
For in the work of this chapter, there is often the evacuation of blood when opening a vein, and incising an abscess, and in the treatment of wounds, and in the extraction of arrows, and in cutting into stones, and similar things; where there is doubt and fear, and many die.
Quant li chiés de l’ajutoire est desaloiez par cause de moistor, et on le remet a leu, et il n’i puet demorer ains revient adés et desalue par petit movement qui avient, si com nos avons esproveit, adonques covient il que tu ramoinnes la dislocation premierement.
When the head of the shoulder is dislocated due to moisture, and it is reset but cannot stay in place, repeatedly dislocating with slight movement as we have experienced, then you must first reset the dislocation.
Dislocations est issue d’aucune jointe de son leu, por coi il ne se puet muevre, et est li membres mal figurez, et sent li malaides grant dolor et grant lesion.
Dislocation occurs when a joint moves out of its place, which prevents it from moving, and the limb is misaligned, causing the patient great pain and injury.
Here comes the first sentence to translate. Do not add any comments or contextual information about the text, like "Here is the translation", don't provide any comments about the text like, "Wow this is hard!", etc. Do not comment on whether the translation is accurate or not, it doesn't matter. Just translate the text line-by-line into English and that should be the only text produced in the final output file and nothing else:
'''

ctx = 2000

for fnum in range(0, 5):
    with open(f"mistral_nemo/mistral_nemo_{fnum}.txt", "w") as outfile:
        response = ollama.generate(model=model, prompt=first_prompt + lines[0], options={"num_ctx": ctx})
        print(f"{lines[0].strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)

        for line in tqdm.tqdm(lines[1:]):
            if "\n" in response['response'] or len(response['context']) > ctx:
                response = ollama.generate(model=model, prompt=first_prompt + line, options={"num_ctx": ctx})
            else:
                response = ollama.generate(model=model, prompt=line, options={"num_ctx": ctx}, context=response['context'])
            if 'context' not in response:
                while 'context' not in response:
                    print("Retrying...", file=sys.stderr)
                    response = ollama.generate(model=model, prompt=first_prompt + line, options={"num_ctx": ctx})
            else:            
                response['context'] = response['context'][len(response['context']) // 2:]
            print(f"{line.strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)
