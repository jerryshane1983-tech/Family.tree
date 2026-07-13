import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

print("Checking Goode descendants...")

# Find CJ, Duffy, Miles IDs
cj_id = "@I441@"
duffy_id = "@I442@"
miles_id = "@I443@"

for p in data["people"]:
    name = p.get("name", "")
    note = p.get("note", "")
    
    if "Goode" in name and "Grandchild of A.J. Goode" in note:
        print(f"Found grandchild: {name} (ID: {p['id']})")
        print(f"Note: {note}")
        print(f"Current Parents: {p.get('parents', [])}")
        print("---")
