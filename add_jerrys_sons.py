import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add Jerry's two sons (Gen 2R)
new_people = [
    {
      "id": "@I603@",
      "name": "Unknown Son 1 (Hacker)",
      "gender": "M",
      "parents": ["@I504@"],
      "note": "1st Cousin 2R (Son of Jerry Wayne Hacker)."
    },
    {
      "id": "@I604@",
      "name": "Unknown Son 2 (Hacker)",
      "gender": "M",
      "parents": ["@I504@"],
      "note": "1st Cousin 2R (Son of Jerry Wayne Hacker)."
    }
]

data["people"].extend(new_people)

# Link them to Jerry Wayne Hacker (@I504@)
for p in data["people"]:
    if p["id"] == "@I504@": # Jerry Wayne Hacker
        if "children" not in p: p["children"] = []
        if "@I603@" not in p["children"]: p["children"].append("@I603@")
        if "@I604@" not in p["children"]: p["children"].append("@I604@")

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
