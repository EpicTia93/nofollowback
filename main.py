# main.py
import json
from urllib.parse import urlparse

def username_from_entry(entry):
    # 1) Instagram "following" export often stores the handle in "title"
    if isinstance(entry, dict) and entry.get("title"):
        return entry["title"].strip()

    # 2) Some exports put it inside string_list_data[0]['value']
    sld = entry.get("string_list_data", []) if isinstance(entry, dict) else []
    if sld:
        first = sld[0]
        if isinstance(first, dict) and first.get("value"):
            return first["value"].strip()

        # 3) Fallback: parse from href
        href = first.get("href")
        if href:
            path = urlparse(href).path  # e.g. "/_u/manuel_fiorello"
            parts = [p for p in path.split("/") if p]
            if parts:
                # Prefer the last segment; for "/_u/user" it's "user"
                return parts[-1].strip()

    return None

def load_entries(obj, likely_keys):
    """Return the first list found among likely_keys, else obj if it's already a list."""
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for k in likely_keys:
            if k in obj and isinstance(obj[k], list):
                return obj[k]
    return []

# --- Process following.json ---
with open("following.json", "r") as f:
    following_obj = json.load(f)

following_entries = load_entries(following_obj, [
    "relationships_following", "following", "data"
])

following_usernames = []
for entry in following_entries:
    u = username_from_entry(entry)
    if u:
        following_usernames.append(u)
    else:
        # Optional: uncomment to debug
        # print("Skipping entry (no username):", entry)
        pass

with open("following.txt", "w") as out:
    for u in following_usernames:
        out.write(u + "\n")

# --- Process followers.json ---
with open("followers.json", "r") as f:
    followers_obj = json.load(f)

followers_entries = load_entries(followers_obj, [
    "relationships_followers", "followers", "data"
])

followers_usernames = []
for entry in followers_entries:
    u = username_from_entry(entry)
    if u:
        followers_usernames.append(u)

with open("followers.txt", "w") as out:
    for u in followers_usernames:
        out.write(u + "\n")

# --- Compute "not following back" ---
with open("following.txt", "r") as f:
    following_set = set(line.strip() for line in f if line.strip())

with open("followers.txt", "r") as f:
    followers_set = set(line.strip() for line in f if line.strip())

noback = sorted(following_set - followers_set)

with open("noback.txt", "w") as out:
    for u in noback:
        out.write(u + "\n")

print("List of users who don't follow you back can be found in noback.txt")
