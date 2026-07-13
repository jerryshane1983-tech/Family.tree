import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Find Scott Self (@I423_1@)
for p in data["people"]:
    if p["id"] == "@I423_1@":
        # Add Shane
        shane_id = "@I423_1_2@"
        if shane_id not in p["children"]:
            p["children"].append(shane_id)
        
        p["note"] = p.get("note", "") + " Has other children whose names are currently unknown."
        
        # Add Shane to people
        data["people"].append({
            "id": shane_id,
            "name": "Shane Self",
            "gender": "M",
            "parents": ["@I423_1@"]
        })
        break

for p in data["people"]:
    if p["id"] in ["@I423@", "@I435@"]: # Oleta and Raymond
        note = p.get("note", "")
        if "May have other children" not in note:
            p["note"] = note + " May have other unknown children besides Scott."
            
with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Added Shane Self to the tree!")
