with open("chatgpt_lat/part1.txt") as enf:
    en_lines = enf.readlines()
with open("lat/all_text.txt") as laf:
    la_lines = laf.readlines()

for i in range(len(en_lines)):
    print(la_lines[i].strip() + "\t" + en_lines[i].strip())
