import re

# Function to switch the bracketed parts
def switch_brackets(line):
    # Use regular expression to find the two bracketed parts (including empty brackets [])
    match = re.findall(r'\[.*?\]', line)
    
    if len(match) == 2:
        # If there are exactly two bracketed parts (including empty), swap them
        return line.replace(match[0], "TEMP_PLACEHOLDER").replace(match[1], match[0]).replace("TEMP_PLACEHOLDER", match[1])
    else:
        # If there aren't exactly two bracketed parts, return the line unchanged
        return line

# Read the file and process each line
def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace and process the line
            processed_line = switch_brackets(line.strip())
            print(processed_line)

# Replace 'your_file.txt' with the path to your actual file
process_file('combined_path_lat_manual.txt')
