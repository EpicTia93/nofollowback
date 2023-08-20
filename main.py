import json

# Load the following.json file
with open('following.json', 'r') as json_file:
    data = json.load(json_file)

# Write each value to a file
with open('following.txt', 'w') as output_file:
    for entry in data['relationships_following']:
        for item in entry['string_list_data']:
            output_file.write(item['value'] + '\n')



# Load the followers.json data from the file
with open('followers.json', 'r') as json_file:
    data = json.load(json_file)

# Extract "value" fields from the JSON data
values = [entry['string_list_data'][0]['value'] for entry in data]

# Write the extracted values to followers.txt
with open('followers.txt', 'w') as txt_file:
    for value in values:
        txt_file.write(value + '\n')



# Read the contents of following.txt and followers.txt
with open('following.txt', 'r') as following_file:
    following = set(following_file.read().splitlines())

with open('followers.txt', 'r') as followers_file:
    followers = set(followers_file.read().splitlines())

# Calculate the differences (users you follow but who don't follow you back)
noback = following - followers

# Write the differences to noback.txt
with open('noback.txt', 'w') as noback_file:
    for user in noback:
        noback_file.write(user + '\n')

print("List of users who don't follow you back can be found in noback.txt file")
