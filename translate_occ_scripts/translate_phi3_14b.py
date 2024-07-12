import ollama
import tqdm

with open("all_text.txt") as f:
    lines = f.readlines()

for fnum in range(3, 10):
    outfile = open(f"phi3/phi3_14b_{fnum}.txt", "w")
    response = ollama.chat(model='phi3:14b', messages=[
        {
            'role': 'user',
            'content': f'''The following text is a medieval medical treatise written in a language that is somwhat similar to Latin, Italian, Spanish and slightly to French as well.
    Try to guess what the text means and translate it line by line into English. Do not add any comments, just reply with the guessed translation.
    Source: Quan dolor de juncturas son faytas per humors fregas les quals so enfundutz a quascun membre del cors, lahoras quan veno dolors en los pes, de costuma dels metges es que aquo apelen podragua propriament.
    English: When joint pain is caused by cold humors that infiltrate each part of the body, and pain occurs in the feet, it is customarily called gout by doctors.
    Source: E si es necessitat que puntz sia fayt sobre la fassia del pe, lahoras fay am cauteri de punt.
    English: And if it is necessary to make points on the surface of the foot, then do so with a pointed cautery.
    Source: E aprop reduzeys le budel o l’atela a la sua conquavitat, e aprop pause la sua ma sobre le loc per so que le budel no yesqua.
    English: Then return the intestine or hernia to its cavity, and place your hand over the area to prevent the intestine from coming out.
    Source: E tu ja has ubert entre las coyssas del malaute e dejos lu as pausat un coyssi, et autre servent sia sus las cambas de lu, e autre sus le pietz de lu, le qual tengua las suas mas.
    English: You have already opened the space between the patient's thighs, placed a cushion under them, another servant on their legs, and another on their chest, holding their hands.
    Source: {lines[0].strip()}
    English: 
    ''',
        },
    ])
    print(lines[0])
    print(response['message']['content'])
    print(f"{lines[0].strip()}\t{response['message']['content'].splitlines()[0].strip()}", file=outfile)

    for line in tqdm.tqdm(lines):
        response = ollama.chat(model='phi3:14b', messages=[
        {
            'role': 'user',
            'content': f'''{line.strip()}
    English: ''',
        },
        ])
        print(f"{line.strip()}\t{response['message']['content'].splitlines()[0].strip()}", file=outfile)
