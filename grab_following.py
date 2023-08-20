# Snippet that creates the following.txt output file
import json

# Load the following.json file
with open('following.json', 'r') as json_file:
    data = json.load(json_file)

# Write each value to a file
with open('following.txt', 'w') as output_file:
    for entry in data['relationships_following']:
        for item in entry['string_list_data']:
            output_file.write(item['value'] + '\n')
