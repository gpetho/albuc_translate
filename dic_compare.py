dictionary = {}

with open("null.dic") as old_dic:
    old_text = old_dic.read().splitlines()

for line in old_text:
    occ, eng = line.strip().split(" @ ")
    dictionary[occ] = eng

with (open("auto_new.dic") as new_dic,
      open("auto_filtered.dic", "w") as filtered):
    new_text = new_dic.read().splitlines()
    for line in new_text:
        occ, eng = line.strip().split(" @ ")
        if dictionary.get(occ) != eng:
            print(line, file=filtered)
