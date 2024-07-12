with (open("chatgpt/converted_all.txt") as chatf,
      open("chatgpt/all_text.txt", 'w') as outf):
    for line in chatf:
        try:
            eng_text = line.split("\t")[1]
        except IndexError:
            print(line)
            break
        outf.write(eng_text)
