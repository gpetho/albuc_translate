import ollama

with open("prompts/mt_eval.txt") as f:
    prompt_template = f.read()

with open("aligned_sl_lat/spink_lewis.ref.txt") as f:
    refs = f.read()

refs = refs.split("\n")

with open("aligned_sl_lat/translations/aya/aya_0.txt") as f:
    hyps = f.read()

hyps = hyps.split("\n")

for i, (ref, hyp) in enumerate(zip(refs, hyps), start=1):
    prompt = prompt_template.format(ref=ref, hyp=hyp)
    print(f"Prompt {i}")
    print(prompt)

    response = ollama.generate(model="llama3.2",
                               prompt=prompt)
    print(response['response'])

    if i == 5:
        break