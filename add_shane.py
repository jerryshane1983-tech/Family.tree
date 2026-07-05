import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Define Shane
new_person = {
    "id": "@I510@",
    "name": "Shane Wesson Hacker",
    "gender": "M",
    "parents": ["@I24@"],
    "note": "1st Cousin 1R (Son of Lisa Hacker)."
}

data["people"].append(new_person)

# Add Shane to Lisa's children array
for p in data["people"]:
    if p["id"] == "@I24@":
        if "children" not in p:
            p["children"] = []
        if "@I510@" not in p["children"]:
            p["children"].append("@I510@")
        break

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
