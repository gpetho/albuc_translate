import re

with open('chapters_standoff.xml') as f:
    lines = f.readlines()

flag = False
for line in lines:
    if "subch2.89" in line:
        flag = True
    if not flag:
        continue

    ## find value of start_s
    m = re.search(r'start_s="s(\d+)"', line)
    ## decrement the value by 2
    if m:
        start_s = int(m.group(1))
        start_s -= 1
        line = re.sub(r'start_s="s\d+"', f'start_s="s{start_s:04d}"', line)
    
    ## find value of end_s
    m = re.search(r'end_s="s(\d+)"', line)
    ## decrement the value by 2
    if m:
        end_s = int(m.group(1))
        end_s -= 1
        line = re.sub(r'end_s="s\d+"', f'end_s="s{end_s:04d}"', line)

    print(line, end='')