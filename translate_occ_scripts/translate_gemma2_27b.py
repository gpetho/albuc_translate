import ollama
import tqdm

with open("all_text.txt") as f:
    lines = f.readlines()

model = 'gemma2:27b-instruct-q6_K'

first_prompt = '''The following text is a medieval medical treatise written in a language that is somewhat similar to Latin, Italian, Spanish and slightly to French as well.
Try to guess what the text means and translate it line by line into English like this:
Source 1: Quan dolor de juncturas son faytas per humors fregas les quals so enfundutz a quascun membre del cors, lahoras quan veno dolors en los pes, de costuma dels metges es que aquo apelen podragua propriament.
Translation 1: When joint pain is caused by cold humors that infiltrate each part of the body, and pain occurs in the feet, it is customarily called gout by doctors.
Source 2: E si es necessitat que puntz sia fayt sobre la fassia del pe, lahoras fay am cauteri de punt.
Translation 2: And if it is necessary to make points on the surface of the foot, then do so with a pointed cautery.
Source 3: E aprop reduzeys le budel o l’atela a la sua conquavitat, e aprop pause la sua ma sobre le loc per so que le budel no yesqua.
Translation 3: Then return the intestine or hernia to its cavity, and place your hand over the area to prevent the intestine from coming out.
Source 4: E tu ja has ubert entre las coyssas del malaute e dejos lu as pausat un coyssi, et autre servent sia sus las cambas de lu, e autre sus le pietz de lu, le qual tengua las suas mas.
Translation 4: You have already opened the space between the patient's thighs, placed a cushion under them, another servant on their legs, and another on their chest, holding their hands.
Here comes the first source sentence to translate:
'''
next_prompt = "Here comes the next source sentence to translate:\n"
prompt_suffix = 'Just reply with a single line containing the guessed translation of this source sentence and nothing else. Do not add any comments before it, like "here is the translation":'

ctx = 4096

for fnum in range(0, 10):
    outfile = open(f"gemma2/gemma2_27b_{fnum}.txt", "w")

    for line in tqdm.tqdm(lines):
        response = ollama.generate(model=model, prompt=first_prompt + line + "\n" + prompt_suffix, options={"num_ctx": ctx})
        if response['response'].strip() == "" or 'context' not in response:
            response = ollama.generate(model=model, prompt=first_prompt + line + "\n" + prompt_suffix, options={"num_ctx": ctx})
        if response['response'].strip() == "":
            print(f"{line.strip()}\t", file=outfile)
        else:
            print(f"{line.strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)
        print(response['response'])

    outfile.close()
