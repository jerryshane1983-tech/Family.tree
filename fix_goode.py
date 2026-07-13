import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Fix Nadine (@I422@) - remove James (@I440@) from children, ensure C.J. (@I441@), Duffy (@I442@), Miles (@I443@) are there
for p in data["people"]:
    if p["id"] == "@I422@":
        if "@I440@" in p.get("children", []):
            p["children"].remove("@I440@")
        
        for child_id in ["@I441@", "@I442@", "@I443@"]:
            if child_id not in p.get("children", []):
                p.setdefault("children", []).append(child_id)
        break

# Fix James Goode (@I440@) - remove Nadine (@I422@) from parents
for p in data["people"]:
    if p["id"] == "@I440@":
        if "@I422@" in p.get("parents", []):
            p["parents"].remove("@I422@")
        break

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed the Goode branch connections!")
