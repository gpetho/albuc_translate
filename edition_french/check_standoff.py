import re

previous_end = 0

with open("updated_standoff.xml") as f:
    for line in f:
        output = line.strip()

        # search for "s\d{4}" in standoff
        s_numbers = re.findall(r'((start|end)_s="s(\d{4})")', line)

        for whole, se, num in s_numbers:
            if se == 'start':
                if int(num) != previous_end + 1:
                    print(f"Start of chapter {num} is not immediately after end of previous chapter {previous_end}")
                start = int(num)
            else:
                if int(num) < start:
                    print(f"End of chapter {num} is before start of chapter {start}")
                previous_end = int(num)