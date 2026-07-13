import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Find Scott Self (@I423_1@)
for p in data["people"]:
    if p["id"] == "@I423_1@":
        # Add Kayelee and Reva
        kayelee_id = "@I423_1_3@"
        reva_id = "@I423_1_4@"
        
        if kayelee_id not in p["children"]:
            p["children"].append(kayelee_id)
        if reva_id not in p["children"]:
            p["children"].append(reva_id)
            
        # Add Kayelee to people
        data["people"].append({
            "id": kayelee_id,
            "name": "Kayelee Self",
            "gender": "F",
            "birth_year": 1999,
            "parents": ["@I423_1@"]
        })
        
        # Add Reva to people
        data["people"].append({
            "id": reva_id,
            "name": "Reva Self",
            "gender": "F",
            "birth_year": 2003,
            "parents": ["@I423_1@"]
        })
        break

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Added Kayelee and Reva to Scott's children!")
