import sys

current_chapter = ''
with (open(f"combined_path_{sys.argv[1]}.txt") as path_f,
      open(f"unaligned{sys.argv[1]}.txt", "w") as unaligned_f):
    for line in path_f:
        if line.strip() == '':
            continue
        if line[0] != '[':
            current_chapter = line.strip()
            print(current_chapter, file=unaligned_f)
        else:
            eng_line, chat_line, score = line.strip().split(':')
            if float(score) > 0:
                continue
            with (open(f"sentalign_input/{sys.argv[1]}/{current_chapter}") as chat_f,
                  open(f"sentalign_input/eng/{current_chapter}") as eng_f):
                chat_text = chat_f.readlines()
                eng_text = eng_f.readlines()
                print(chat_line, eng_line, file=unaligned_f)
                if chat_line == '[]':
                    for line in eng_line[1:-1].split(','):
                        print(eng_text[int(line)], file=unaligned_f)
                else:
                    for line in chat_line[1:-1].split(','):
                        print(chat_text[int(line)], file=unaligned_f)
