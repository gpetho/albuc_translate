#Modified script to run ChirAlb through Gemma2 on Google Cloud TPU

import os
import ollama
import tqdm

# Ensure the file exists
file_path = "chiralb.txt"
try:
    with open(file_path, "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
    exit(1)

# Check if the file is empty
if not lines:
    print(f"Error: The file {file_path} is empty.")
    exit(1)

ctx = 4096
model = 'gemma2:9b'

first_prompt = '''The following text is a medieval medical treatise written in Old French, around the 12th-13th centuries.
Try to guess what the text means and translate it line by line into English like this:
When chronic pain comes in the whole head and lasts a long time, the patient should use salves and pills called "cochie", and purgatives for the head and oils and plasters; and if the cautery we mentioned before is applied and it does not work.
Here comes the first sentence to translate. Do not add any comments or contextual information about the text, like "Here is the translation", just reply with the guessed translation and nothing else:
'''

# Create an output directory if it doesn't exist
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Process each line
for fnum in range(0, 10):
    with open(f"{output_dir}/gemma2_9b_{fnum}.txt", "w") as outfile:
        response = ollama.generate(
            model=model,
            prompt=first_prompt + lines[0],
            options={"num_ctx": ctx}
        )
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

print("Translation complete. Output written to the output directory.")