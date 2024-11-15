import re

old_to_start = {}
old_to_end = {}

with open("too_long_to_new.txt") as f:
    for line in f:
        old, start, end = line.strip().split()
        old_to_start[int(old)] = int(start)
        old_to_end[int(old)] = int(end)

with open("updated_standoff.xml") as f:
    for line in f:

        output = line.strip()

        # search for "s\d{4}" in standoff
        s_numbers = re.findall(r'((start|end)_s="s(\d{4})")', line)

        for whole, se, num in s_numbers:
            old_number = int(num)
            if se == 'start':
                new_number = old_to_start[old_number]
            else:
                new_number = old_to_end[old_number]
            output = output.replace(whole, f'{se}_s="s{new_number:04d}"', 1)

        print(output)
