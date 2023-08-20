// Snippet that creates the followers.txt output file
import json

# Load the followers.json data from the file
with open('followers.json', 'r') as json_file:
    data = json.load(json_file)

# Extract "value" fields from the JSON data
values = [entry['string_list_data'][0]['value'] for entry in data]

# Write the extracted values to followers.txt
with open('followers.txt', 'w') as txt_file:
    for value in values:
        txt_file.write(value + '\n')
