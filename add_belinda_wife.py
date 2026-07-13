import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Find Scott Self (@I423_1@)
for p in data["people"]:
    if p["id"] == "@I423_1@":
        p["spouse"] = "Belinda Self"
        # Update note since we identified his wife
        note = p.get("note", "")
        p["note"] = note + " Wife identified as Belinda Self via OSINT/User confirmation."
        break

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Added Belinda as Scott's wife!")
