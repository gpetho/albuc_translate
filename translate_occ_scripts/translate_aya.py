import ollama
import tqdm

with open("all_text.txt") as f:
    lines = f.readlines()

model = 'aya:8b'

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

ctx = 6144

for fnum in range(0, 10):
    outfile = open(f"aya/aya_8b_{fnum}.txt", "w")

    response = ollama.generate(model=model, prompt=first_prompt + lines[0], options={"num_ctx": ctx})
    print(f"{lines[0].strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)

    for line in tqdm.tqdm(lines[1:]):
        if len(response['context']) > 4096:
            response = ollama.generate(model=model, prompt=first_prompt + line, options={"num_ctx": ctx})
        else:
            response = ollama.generate(model=model, prompt=line, options={"num_ctx": ctx}, context=response['context'])
        if response['response'].strip() == "" or 'context' not in response:
            response = ollama.generate(model=model, prompt=first_prompt + line, options={"num_ctx": ctx})
        if response['response'].strip() == "":
            print(f"{line.strip()}\t", file=outfile)
        else:
            print(f"{line.strip()}\t{response['response'].splitlines()[0].strip()}", file=outfile)

    outfile.close()
