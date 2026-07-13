import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Find Oleta (@I423@) and Raymond (@I435@)
oleta = None
raymond = None

for p in data["people"]:
    if p["id"] == "@I423@":
        oleta = p
    elif p["id"] == "@I435@":
        raymond = p

if oleta and raymond:
    # Ensure they have a children array
    if "children" not in oleta:
        oleta["children"] = []
    if "children" not in raymond:
        raymond["children"] = []

    # Add Scott Self if not present
    scott_id = "@I423_1@"
    if scott_id not in oleta["children"]:
        oleta["children"].append(scott_id)
        raymond["children"].append(scott_id)
        
        # Add Scott to people
        data["people"].append({
            "id": scott_id,
            "name": "Scott Self",
            "gender": "M",
            "parents": ["@I423@", "@I435@"],
            "children": ["@I423_1_1@"]
        })
        
        # Add Rebekah to people
        data["people"].append({
            "id": "@I423_1_1@",
            "name": "Rebekah Susanne \"Suzi\" (Self) Wilkenson",
            "gender": "F",
            "parents": [scott_id]
        })

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Added Scott Self and Rebekah Susanne to the tree!")
