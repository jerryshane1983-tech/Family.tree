import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Remove Michael from Curtiss's children
for p in data["people"]:
    if p["id"] == "@I427@":
        if "@I434@" in p.get("children", []):
            p["children"].remove("@I434@")
        break

# Remove Michael's object
data["people"] = [p for p in data["people"] if p["id"] != "@I434@"]

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Removed Michael Curtiss Nipp")
