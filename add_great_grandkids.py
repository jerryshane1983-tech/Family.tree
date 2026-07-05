import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add Hayden and Baylee (Gen 2R)
new_people = [
    {
      "id": "@I601@",
      "name": "Hayden",
      "gender": "M",
      "parents": ["@I506@"],
      "note": "1st Cousin 2R (Son of Summer)."
    },
    {
      "id": "@I602@",
      "name": "Baylee",
      "gender": "F",
      "parents": ["@I507@"],
      "note": "1st Cousin 2R (Daughter of Amber)."
    }
]

data["people"].extend(new_people)

# Link them to their mothers
for p in data["people"]:
    if p["id"] == "@I506@": # Summer
        if "children" not in p: p["children"] = []
        if "@I601@" not in p["children"]: p["children"].append("@I601@")
    elif p["id"] == "@I507@": # Amber
        if "children" not in p: p["children"] = []
        if "@I602@" not in p["children"]: p["children"].append("@I602@")

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
