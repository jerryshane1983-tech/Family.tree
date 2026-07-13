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
    # Add siblings (Richard, Radonna, Raymond Jr)
    siblings = [
        {"id": "@I423_2@", "name": "Richard Self", "gender": "M", "birth_year": 1962},
        {"id": "@I423_3@", "name": "Radonna Self", "gender": "F", "birth_year": 1964},
        {"id": "@I423_4@", "name": "Raymond Self", "gender": "M", "birth_year": 1966}
    ]
    
    for sib in siblings:
        if sib["id"] not in oleta["children"]:
            oleta["children"].append(sib["id"])
        if sib["id"] not in raymond["children"]:
            raymond["children"].append(sib["id"])
            
        # Check if they exist in people array
        exists = False
        for p in data["people"]:
            if p["id"] == sib["id"]:
                exists = True
                break
        
        if not exists:
            sib["parents"] = ["@I423@", "@I435@"]
            sib["note"] = "Added via OSINT public directory scan. Relationship deduced by age."
            data["people"].append(sib)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Added deduced siblings to tree!")
