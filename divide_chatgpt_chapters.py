import os

with open("chatgpt/all_text.txt") as chatgpt_all:
    chatgpt_all_text = chatgpt_all.readlines()
chapters = [f for f in os.listdir('sentalign_input/eng')]

for chapter in chapters:
    with open(f"lines_occ/{chapter}") as occ_lines:
        chapter_lines = occ_lines.readlines()
    chapter_lines = [int(line.strip()) for line in chapter_lines]

    with open(f"sentalign_input/deu/{chapter}", "w") as chatgpt_chapter:
        for line in chapter_lines:
            chatgpt_chapter.write(chatgpt_all_text[line])
