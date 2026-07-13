import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Update Curtiss Nipp (@I427@)
for p in data["people"]:
    if p["id"] == "@I427@":
        if "children" not in p:
            p["children"] = []
        if "@I435@" not in p["children"]:
            p["children"].append("@I435@")
        if "@I436@" not in p["children"]:
            p["children"].append("@I436@")
        break

# Add Justin and Travis
new_people = [
    {
        "id": "@I435@",
        "name": "Justin Nipp",
        "gender": "M",
        "parents": ["@I427@"]
    },
    {
        "id": "@I436@",
        "name": "Travis Nipp",
        "gender": "M",
        "parents": ["@I427@"]
    }
]

# Check if they exist to avoid duplicates
existing_ids = {p["id"] for p in data["people"]}
for np in new_people:
    if np["id"] not in existing_ids:
        data["people"].append(np)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Added Justin and Travis to Curtiss Nipp!")
