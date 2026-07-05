import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add Katelynn's two sons (Gen 2R)
new_people = [
    {
      "id": "@I605@",
      "name": "Unknown Son 1 (Katelynn's)",
      "gender": "M",
      "parents": ["@I508@"],
      "note": "1st Cousin 2R (Son of Katelynn Hacker)."
    },
    {
      "id": "@I606@",
      "name": "Unknown Son 2 (Katelynn's)",
      "gender": "M",
      "parents": ["@I508@"],
      "note": "1st Cousin 2R (Son of Katelynn Hacker)."
    }
]

data["people"].extend(new_people)

# Link them to Katelynn Hacker (@I508@)
for p in data["people"]:
    if p["id"] == "@I508@": # Katelynn
        if "children" not in p: p["children"] = []
        if "@I605@" not in p["children"]: p["children"].append("@I605@")
        if "@I606@" not in p["children"]: p["children"].append("@I606@")

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
