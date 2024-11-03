import os

# Path to the main directory
main_dir = 'lat_translations'


def combine_columns(lines):
    column1 = []
    column2 = []
    for line in lines:
        split_line = line.split("\t")
        column1.append(split_line[0].strip())
        column2.append(split_line[1].strip())
    return ' '.join(column1) + '\t' + ' '.join(column2) + '\n'


# Iterate through each subdirectory in the main directory
for subdir in os.listdir(main_dir):
    subdir_path = os.path.join(main_dir, subdir)
    
    # Ensure we are dealing with a directory
    if os.path.isdir(subdir_path):
        # Iterate through each file in the subdirectory
        for f in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, f)
            
            # Ensure we are dealing with a file
            if os.path.isfile(file_path):
                # Print the file path
                print(file_path)
                
                # Count lines in the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    if len(lines) == 4060:
                        new_lines = lines[:1657]
                        new_lines.append(combine_columns(lines[1657:1659]))
                        new_lines += lines[1659:1863]
                        new_lines.append(combine_columns(lines[1863:1868]))
                        new_lines += lines[1868:]
                        with open(file_path, 'w') as new_file:
                            new_file.writelines(new_lines)
