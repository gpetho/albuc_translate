import spacy

nlp = spacy.load("xx_ent_wiki_sm")

for lang in ("eng", "occ", "lat", "ofr"):
    with (open(f"../{lang}/all_text.txt", "r", encoding="utf-8") as infile,
          open(f"{lang}_vertical.txt", "w", encoding="utf-8") as outfile):
        for i, line in enumerate(infile.readlines()):
            print(f'<s id="{i}">', file=outfile)
            doc = nlp(line.strip())
            for token in doc:
                print(token.text, file=outfile)
            print("</s>", file=outfile)
