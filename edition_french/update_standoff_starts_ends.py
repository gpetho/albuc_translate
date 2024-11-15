import re

with open("chapters_combined_too_long.xml") as ch_f:
    chapter_doc = ch_f.read()

with open("ChirAlbT_text_bfm_mod.xml") as new_xml:
    new_doc = new_xml.read()

with open("chapters_standoff.xml") as f:
    for line in f:
        output = line.strip()

        # search for "s\d{4}" in standoff
        s_numbers = re.findall(r'((start|end)_s="s(\d{4})")', line)

        pattern = 's id="s0000">'

        for whole, se, num in s_numbers:
            chapter_start_idx = chapter_doc.find(f's id="s{num}"') + len(pattern)
#            print(chapter_start_idx)
            chapter_start = chapter_doc[chapter_start_idx:chapter_start_idx + 20]
#            print(chapter_start)
            new_start_idx = new_doc.find(chapter_start)
#            print(new_start_idx)
            if new_start_idx == -1:
                new_id = "****"
            else:
                new_id = '+' + new_doc[new_start_idx-6:new_start_idx-2]
#                print(new_id)

            output = output.replace(whole, f'{se}_s="s{new_id}"', 1)
        #     old_number = int(num)
        #     if se == 'start':
        #         new_number = old_to_start[old_number]
        #     else:
        #         new_number = old_to_end[old_number]
        #     output = output.replace(whole, f'{se}_s="s{new_number:04d}"', 1)

        print(output)

