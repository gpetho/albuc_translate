with (open("chiralb-com.txt") as infile,
      open("../ofr/all_text.txt", 'w') as all_file,
      open("converted_all.txt", 'w') as chatgpt_file):
    chiralb = infile.readlines()
    chapter = ""
    lang = "fr"
    for line in chiralb:
        if line.strip() == "":
            continue
        if line.strip() == "Prologue":
            chapter_file = open("../ofr/preface.txt", 'w')
        elif line.strip() in ("1.", "2.", "3."):
            chapter_file.close()
            chapter = line[0]
            chapter_file = open(f"../ofr/chapter-{chapter}.txt", 'w')
            subchapter = 0
        elif line.strip().startswith(f"{chapter}."):
            chapter_file.close()
            try:
                new_subchapter = int(line.strip().split(".")[-1])
            except ValueError:
                print(f"Error in line {line}")
            if new_subchapter != subchapter + 1:
                print(f"Missing subchapter {subchapter + 1} in chapter {chapter}")
            subchapter = new_subchapter
            chapter_file = open(f"../ofr/chapter-{chapter}-subchapter-{subchapter}.txt", 'w')
        else:
            if lang == "fr":
                chatgpt_file.write(line.strip() + "\t")
                all_file.write(line)
                chapter_file.write(line)
                lang = "en"
            else:
                chatgpt_file.write(line)
                lang = "fr"
    chapter_file.close()