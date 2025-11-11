import sys

indirect_pairs = [
    ("noske_alignment_occ_eng.txt", "noske_alignment_eng_lat.txt",
     "noske_alignment_occ_lat.txt"),
    ("noske_alignment_occ_eng.txt", "noske_alignment_eng_ofr.txt",
     "noske_alignment_occ_ofr.txt"),
    ("noske_alignment_lat_eng.txt", "noske_alignment_eng_ofr.txt",
     "noske_alignment_lat_ofr.txt"),
]

def write_output_kv(key, value, last_output, file):
    sorted_values = sorted(list(set(value)))
    key_str = ""
    value_str = ""
    if len(key) == 1:
        key_str = str(key[0])
    elif len(key) > 1:
        key_str = f"{key[0]},{key[-1]}"
    if not sorted_values:
        value_str = "-1"
    elif len(sorted_values) == 1:
        value_str = str(sorted_values[0])
    elif len(sorted_values) > 1:
        value_str = f"{sorted_values[0]},{sorted_values[-1]}"
    if key_str:
        if sorted_values:
            for output in range(last_output + 1, sorted_values[0]):
                print(f"-1\t{output}", file=file)
            last_output = sorted_values[-1]
        print(f"{key_str}\t{value_str}", file=file)
    key.clear()
    value.clear()
    return last_output

for left_file, middle_file, output_file in indirect_pairs:
    aligned_pairs = {}
    with open("../" + middle_file) as middle_alignment:
        for line in middle_alignment:
            if not line.strip():
                print(f"Warning: Empty line in indirect alignment file {middle_file}")
                sys.exit(1)
            middle_segment, right_segment = line.strip().split("\t")
            keys = []
            values = []
            if middle_segment.isdigit() and int(middle_segment) >= 0:
                keys = [int(middle_segment)]
            elif "," in middle_segment:
                start, end = middle_segment.split(",")
                keys = list(range(int(start), int(end) + 1))
            if right_segment.isdigit() and int(right_segment) >= 0:
                for key in keys:
                    aligned_pairs[key] = [int(right_segment)]
            elif "," in right_segment:
                start, end = right_segment.split(",")
                values = list(range(int(start), int(end) + 1))
                for key in keys:
                    aligned_pairs[key] = values
    with open(output_file + "pairs.txt", "w") as pair_file:
        for k, v in aligned_pairs.items():
            print(f"{k}\t{v}", file=pair_file)
    with (open(left_file) as left_alignment,
          open(output_file, "w") as output_alignment):
        left_key = []
        value = []
        last_output = -1
        for left_line in left_alignment.readlines():
            left_segment, middle_segment = left_line.strip().split("\t")
            if left_segment == "-1":
                # print("Case 1", file=output_alignment)
                last_output = write_output_kv(left_key, value, last_output, output_alignment)
                middle_segment = int(middle_segment)
                if middle_segment in aligned_pairs:
                    for right_segment in aligned_pairs[middle_segment]:
                        last_output = write_output_kv([-1], [right_segment], last_output, output_alignment)
            elif left_segment.isdigit():
                if middle_segment == "-1":
                    # print("Case 2", file=output_alignment)
                    last_output = write_output_kv(left_key, value, last_output, output_alignment)
                    left_key = [int(left_segment)]
                    last_output = write_output_kv(left_key, [], last_output, output_alignment)
                elif middle_segment.isdigit():
                    middle_segment = int(middle_segment)
                    if middle_segment in aligned_pairs:
                        output_segments = aligned_pairs[middle_segment]
                        if output_segments[0] in value:
                            left_key.append(int(left_segment))
                            value.extend(output_segments)
                        else:
                            # print("Case 3", file=output_alignment)
                            last_output = write_output_kv(left_key, value, last_output, output_alignment)
                            left_key = [int(left_segment)]
                            value.extend(output_segments)
                    else:
                        # print("Case 4", file=output_alignment)
                        last_output = write_output_kv(left_key, value, last_output,
                                                      output_alignment)
                        left_key = [int(left_segment)]
                        last_output = write_output_kv(left_key, [], last_output, output_alignment)
                elif "," in middle_segment:
                    start, end = middle_segment.split(",")
                    middle_indices = list(range(int(start), int(end) + 1))
                    overlap = False
                    for mid_idx in middle_indices:
                        aligned_segs = aligned_pairs.get(mid_idx, [])
                        if any(seg in value for seg in aligned_segs):
                            overlap = True
                    if overlap:
                        # print("overlap: left_segment", left_segment, "middle_segment", middle_segment, file=output_alignment)
                        left_key.append(int(left_segment))
                        for mid_idx in middle_indices:
                            value.extend(aligned_pairs.get(mid_idx, []))
                    else:
                        # print("Case 5", file=output_alignment)
                        last_output = write_output_kv(left_key, value, last_output, output_alignment)
                        left_key = [int(left_segment)]
                        for mid_idx in middle_indices:
                            value.extend(aligned_pairs.get(mid_idx, []))
            elif "," in left_segment:
                start, end = left_segment.split(",")
                left_indices = list(range(int(start), int(end) + 1))
                if middle_segment.isdigit():
                    middle_segment = int(middle_segment)
                    if middle_segment in aligned_pairs:
                        output_segments = aligned_pairs[middle_segment]
                        overlap = False
                        for out_seg in output_segments:
                            if out_seg in value:
                                overlap = True
                        if overlap:
                            left_key.extend(left_indices)
                            value.extend(output_segments)
                        else:
                            # print("Case 6", file=output_alignment)
                            last_output = write_output_kv(left_key, value, last_output, output_alignment)
                            left_key = left_indices
                            value.extend(output_segments)
                    else:
                        # print("Case 7", file=output_alignment)
                        last_output = write_output_kv(left_key, value, last_output, output_alignment)
                        for left_idx in left_indices:
                            left_key = [left_idx]
                            last_output = write_output_kv(left_key, [], last_output, output_alignment)
                else:
                    start, end = middle_segment.split(",")
                    middle_indices = list(range(int(start), int(end) + 1))
                    overlap = False
                    for mid_idx in middle_indices:
                        aligned_segs = aligned_pairs.get(mid_idx, [])
                        if any(seg in value for seg in aligned_segs):
                            overlap = True
                    if overlap:
                        left_key.extend(left_indices)
                        for mid_idx in middle_indices:
                            value.extend(aligned_pairs.get(mid_idx, []))
                    else:
                        # print("Case 8", file=output_alignment)
                        last_output = write_output_kv(left_key, value, last_output, output_alignment)
                        left_key = left_indices
                        for mid_idx in middle_indices:
                            value.extend(aligned_pairs.get(mid_idx, []))
