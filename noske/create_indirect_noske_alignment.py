import sys

DEBUG = False

indirect_pairs = [
    ("noske_alignment_occ_eng.txt", "noske_alignment_eng_lat.txt",
     "noske_alignment_occ_lat_debug.txt"),
    ("noske_alignment_occ_eng.txt", "noske_alignment_eng_ofr.txt",
     "noske_alignment_occ_ofr_debug.txt"),
    ("noske_alignment_lat_eng.txt", "noske_alignment_eng_ofr.txt",
     "noske_alignment_lat_ofr_debug.txt"),
]

def write_output_kv(key, value, last_output, file, debug_info=""):
    if not key and not value:  # this is expected for the first line of the alignment file, so we can just return last_output
        return last_output
    assert key, "Key list is empty: " + debug_info
    assert value, "Value list is empty: " + debug_info
    assert key == sorted(list(set(key))), "Key list is not sorted: " + debug_info
    assert key[0] > last_output[0], "Key list does not follow last output: " + debug_info
    sorted_values = sorted(list(set(value)))
    assert sorted_values[0] > last_output[1], "Value list does not follow last output: " + debug_info
    value_str = ""
    if len(key) == 1:
        key_str = str(key[0])
    else:  # if len(key) > 1:
        key_str = f"{key[0]},{key[-1]}"
    if len(sorted_values) == 1:
        value_str = str(sorted_values[0])
    elif len(sorted_values) > 1:
        value_str = f"{sorted_values[0]},{sorted_values[-1]}"
    unaligned_left = range(last_output[0] + 1, key[0])
    unaligned_right = range(last_output[1] + 1, sorted_values[0])
    for u in unaligned_left:
        print(f"{u}\t-1{f'\t{debug_info}\tfor left' if DEBUG else ''}", file=file)
    for u in unaligned_right:
        print(f"-1\t{u}{f'\t{debug_info}\tfor right' if DEBUG else ''}", file=file)
    print(f"{key_str}\t{value_str}{f'\t{debug_info}' if DEBUG else ''}", file=file)
    return key[-1], sorted_values[-1]

for left_file, middle_file, output_file in indirect_pairs:
    aligned_pairs = {}
    # Keep track of the last left and right segment index
    # seen in the left and middle alignment file respectively
    # print unaligned segments at the end after having printed
    # all aligned segments
    left_last = -1
    right_last = -1
    with open(middle_file) as middle_alignment:
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
                last_right = int(right_segment)
                for key in keys:
                    aligned_pairs[key] = [int(right_segment)]
            elif "," in right_segment:
                start, end = right_segment.split(",")
                last_right = int(end)
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
        last_output = (-1, -1) # input side, output side
        for left_line in left_alignment.readlines():
            if DEBUG:
                print(f"Processing line: {left_line.strip()}", file=sys.stderr)
            left_segment, middle_segment = left_line.strip().split("\t")
            if left_segment == "-1" or middle_segment == "-1":
                continue
            if left_segment.isdigit():
                if middle_segment.isdigit():
                    left_digit = int(left_segment)
                    if left_digit != -1:
                        left_last = left_digit
                    middle_segment = int(middle_segment)
                    if left_digit == -1 or middle_segment == -1:
                        continue
                    if middle_segment in aligned_pairs:
                        output_segments = aligned_pairs[middle_segment]
                        if output_segments[0] in value:
                            # input is aligned to an output segment that
                            # is already in the value list, so we have an overlap
                            left_key.append(left_digit)
                            value.extend(output_segments)
                        else:
                            # Input is aligned to an output segment that is not
                            # in the value list, so we have a new alignment.
                            # The previous alignment can be written out.
                            last_output = write_output_kv(left_key, value, last_output, output_alignment, f"case3 {left_line.strip()}")
                            left_key = [left_digit]
                            value = output_segments.copy()
                elif "," in middle_segment:
                    start, end = middle_segment.split(",")
                    middle_indices = list(range(int(start), int(end) + 1))
                    overlap = False
                    if not any(mid_idx in aligned_pairs for mid_idx in middle_indices):
                        # No output segments aligned to any of the middle segments, so we can skip this line 
                        continue
                    for mid_idx in middle_indices:
                        aligned_segs = aligned_pairs.get(mid_idx, [])
                        if any(seg in value for seg in aligned_segs):
                            overlap = True
                    if overlap:
                        # at least one output segment aligned indirectly to the
                        # input segment is already in the value list
                        # print("overlap: left_segment", left_segment, "middle_segment", middle_segment, file=output_alignment)
                        left_key.append(int(left_segment))
                        for mid_idx in middle_indices:
                            value.extend(aligned_pairs.get(mid_idx, []))
                    else:
                        # Input is aligned to output segments that are
                        # not in the value list, so we have a new alignment.
                        # print("Case 5", file=output_alignment)
                        last_output = write_output_kv(left_key, value, last_output, output_alignment, f"case5 {left_line.strip()}")
                        left_key = [int(left_segment)]
                        value = []
                        for mid_idx in middle_indices:
                            value.extend(aligned_pairs.get(mid_idx, []))
            elif "," in left_segment:
                start, end = left_segment.split(",")
                left_indices = list(range(int(start), int(end) + 1))
                left_last = int(end)
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
                            last_output = write_output_kv(left_key, value, last_output, output_alignment, f"case6 {left_line.strip()}")
                            left_key = left_indices
                            value = output_segments.copy()
                else:
                    start, end = middle_segment.split(",")
                    middle_indices = list(range(int(start), int(end) + 1))
                    overlap = False
                    if not any(mid_idx in aligned_pairs for mid_idx in middle_indices):
                        # No output segments aligned to any of the middle segments, so we can skip this line 
                        continue
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
                        last_output = write_output_kv(left_key, value, last_output, output_alignment, f"case8 {left_line.strip()}")
                        left_key = left_indices
                        value = []
                        for mid_idx in middle_indices:
                            value.extend(aligned_pairs.get(mid_idx, []))
        # Write out any remaining alignment after processing all lines
        last_output = write_output_kv(left_key, value, last_output, output_alignment, "final")

        # Write out any unaligned segments at the end after processing all aligned lines
        for left_unaligned in range(last_output[0] + 1, left_last + 1):
            print(f"{left_unaligned}\t-1\t{'final unaligned' if DEBUG else ''}", file=output_alignment)
        for right_unaligned in range(last_output[1] + 1, last_right + 1):
            print(f"-1\t{right_unaligned}\t{'final unaligned' if DEBUG else ''}", file=output_alignment)
