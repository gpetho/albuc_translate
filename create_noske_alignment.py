import re
from collections import Counter
import sys

inputs_outputs = [
    ("combined_path_manual.txt",
     "noske_alignment_occ_eng.txt", "noske_alignment_eng_occ.txt",
     "occ", "eng"),
    ("combined_path_lat_manual.txt",
     "noske_alignment_lat_eng.txt", "noske_alignment_eng_lat.txt",
     "lat", "eng"),
    ("combined_path_ofr_manual.txt",
     "noske_alignment_ofr_eng.txt", "noske_alignment_eng_ofr.txt",
     "ofr", "eng")
]

for input_file, output_file, reverse_file, left_dir, right_dir in inputs_outputs:
    with (open(input_file) as alignment_file,
          open(output_file, "w") as output_file,
          open(reverse_file, "w") as reverse_output):
        left_text = []
        right_text = []
        left_seen = Counter()
        right_seen = Counter()
        left_aligned = 0
        right_aligned = 0
        start_left = 0
        start_right = 0
        left_last = -1
        right_last = -1
        reverse_right = ""
        for line in alignment_file.readlines():
            if line.startswith("["):
                match = re.match(r"\[([0-9,]*)\]:\[([0-9,]*)\]", line)
                if match:
                    left, right = match.groups()
                    print(left, right)
                    if not left:
                        print("-1")
                        output_file.write("-1\t")
                        reverse_right = "-1"
                    elif left.isdigit():
                        print(left_text[int(left)].strip())
                        reverse_right = str(int(left) + start_left)
                        output_file.write(reverse_right + "\t")
                        if int(left) < left_last:
                            print(f"Warning: Left index {left} smaller than last {left_last}")
                            print(input_file)
                            print(current_file)
                            sys.exit(1)
                        left_last = int(left)
                        left_seen[int(left)] += 1
                        left_aligned += 1
                    else:
                        left_indices = sorted(list(set([int(i) for i in left.split(",")])))
                        reverse_right = f"{left_indices[0] + start_left},{left_indices[-1] + start_left}"
                        output_file.write(f"{reverse_right}\t")
                        for idx in left_indices:
                            print(left_text[idx].strip())
                            left_seen[idx] += 1
                            if idx < left_last:
                                print(f"Warning: Left index {idx} smaller than last {left_last}")
                                print(input_file)
                                print(current_file)
                                sys.exit(1)
                            left_last = idx
                        left_aligned += len(left_indices)
                    if not right:
                        print("-1")
                        print("-1", file=output_file)
                        reverse_output.write("-1\t" + reverse_right + "\n")
                    elif right.isdigit():
                        print(right_text[int(right)])
                        print(int(right) + start_right, file=output_file)
                        reverse_output.write(f"{int(right) + start_right}\t" + reverse_right + "\n")
                        if int(right) < right_last:
                            print(f"Warning: Right index {right} smaller than last {right_last}")
                            print(input_file)
                            print(current_file)
                            sys.exit(1)
                        right_last = int(right)
                        right_seen[int(right)] += 1
                        right_aligned += 1
                    else:
                        right_indices = sorted(list(set([int(i) for i in right.split(",")])))
                        print(f"{right_indices[0] + start_right},{right_indices[-1] + start_right}", file=output_file)
                        reverse_output.write(f"{right_indices[0] + start_right},{right_indices[-1] + start_right}\t"
                                             + reverse_right + "\n")
                        for idx in right_indices:
                            print(right_text[idx].strip())
                            right_seen[idx] += 1
                            if idx < right_last:
                                print(f"Warning: Right index {idx} smaller than last {right_last}")
                                print(input_file)
                                print(current_file)
                                sys.exit(1)
                            right_last = idx
                        right_aligned += len(right_indices)
                else:
                    print("Malformed alignment line:", line)
                print()
            elif line.strip():
                current_file = line.strip()
                print(f"Processing file: {current_file}")
                with open(f"{left_dir}/{current_file}") as left_file:
                    left_text = left_file.readlines()
                with open(f"{right_dir}/{current_file}") as right_file:
                    right_text = right_file.readlines()
                left_aligned = 0
                right_aligned = 0
            else:
                stop = False
                if left_aligned != len(left_text):
                    print(
                        f"Warning: Not all left lines aligned in {current_file}: {left_aligned}/{len(left_text)}"
                    )
                    stop = True
                if right_aligned != len(right_text):
                    print(
                        f"Warning: Not all right lines aligned in {current_file}: {right_aligned}/{len(right_text)}"
                    )
                    stop = True
                for i in range(len(left_text)):
                    if left_seen[i] > 1:
                        print(f"Warning: Left line {i} in {current_file} aligned {left_seen[i]} times")
                        stop = True
                    elif left_seen[i] == 0:
                        print(f"Warning: Left line {i} in {current_file} not aligned")
                        stop = True
                for i in range(len(right_text)):
                    if right_seen[i] > 1:
                        print(f"Warning: Right line {i} in {current_file} aligned {right_seen[i]} times")
                        stop = True
                    elif right_seen[i] == 0:
                        print(f"Warning: Right line {i} in {current_file} not aligned")
                        stop = True
                if stop:
                    sys.exit(1)
                start_left += left_aligned
                start_right += right_aligned
                left_last = -1
                right_last = -1
                left_seen = Counter()
                right_seen = Counter()
