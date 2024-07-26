import ollama
import tqdm
import os

# Ensure the directory exists
os.makedirs("phi3-14b", exist_ok=True)

with open("chiralb.txt") as f:
    lines = f.readlines()

for fnum in range(3, 10):
    with open(f"phi3-14b/phi3_14b_{fnum}.txt", "w") as outfile:
        response = ollama.chat(model='phi3:14b', messages=[
            {
                'role': 'user',
                'content': '''The following text is a medieval medical treatise written in Old French, around the 12th-13th centuries.
                    Try to guess what the text means and translate it line by line into English like this:
                    Ou cautere de feu comande au malaide qu’il laisse les poilz tant qu’il soient lons et igals; et s’il le poignent a lor nassance, se li estraint les eulz qu’il ne se muevent tant qu’il naissent.
                    For the fire cautery, instruct the patient to let the hairs grow long and even; and if they prick at their base, hold the eyes steady so they do not move until they grow.
                    Car en l’ovraige de cest chapistre avient maintes fois evacuation de sanc a l’ovrir la voinne, et a l’incision sus aposteme, et as cures des plaies, et a l’estraction des saiettes, et a l’incision sus la piere, et les semblans choses; ou il a doutance et paor, et en vient li mors a plusors. 
                    For in the work of this chapter, there is often the evacuation of blood when opening a vein, and incising an abscess, and in the treatment of wounds, and in the extraction of arrows, and in cutting into stones, and similar things; where there is doubt and fear, and many die.
                    Quant li chiés de l’ajutoire est desaloiez par cause de moistor, et on le remet a leu, et il n’i puet demorer ains revient adés et desalue par petit movement qui avient, si com nos avons esproveit, adonques covient il que tu ramoinnes la dislocation premierement.
                    When the head of the shoulder is dislocated due to moisture, and it is reset but cannot stay in place, repeatedly dislocating with slight movement as we have experienced, then you must first reset the dislocation.
                    Here comes the first sentence to translate. Do not add any comments or contextual information about the text, like "Here is the translation", don't provide any comments about the text like, "Wow this is hard!", etc. Do not comment on whether the translation is accurate or not, it doesn't matter. Just translate the text line-by-line into English and that should be the only text produced in the final output file and nothing else:
                ''' + lines[0].strip(),
            },
        ])
        print(lines[0].strip())
        print(response['message']['content'].strip())
        print(f"{lines[0].strip()}\t{response['message']['content'].strip()}", file=outfile)

        for line in tqdm.tqdm(lines[1:]):
            response = ollama.chat(model='phi3:14b', messages=[
                {
                    'role': 'user',
                    'content': f'''{line.strip()}
    English: ''',
                },
            ])
            print(f"{line.strip()}\t{response['message']['content'].splitlines()[0].strip()}", file=outfile)
