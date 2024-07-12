with (open("occ/all_text.txt") as occ_text,
    open("claude/sonnet_converted.txt") as bitext):
    occ_lines = occ_text.readlines()
    bitext_lines = bitext.readlines()

for i, (occ_line, bitext_line) in enumerate(zip(occ_lines, bitext_lines)):
    if bitext_line.lstrip()[:5] != occ_line.lstrip()[:5]:
        print(i)
        print(occ_line.lstrip())
        print(bitext_line.lstrip())
        break

