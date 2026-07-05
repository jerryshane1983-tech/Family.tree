import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add Madisyn Paige and Marley Peyton
new_people = [
    {
      "id": "@I700@",
      "name": "Madisyn Paige Sanderson",
      "gender": "F",
      "parents": ["@I1@"],
      "note": "Daughter."
    },
    {
      "id": "@I701@",
      "name": "Marley Peyton Sanderson",
      "gender": "F",
      "parents": ["@I1@"],
      "note": "Daughter."
    }
]

data["people"].extend(new_people)

# Link them to the user (@I1@)
for p in data["people"]:
    if p["id"] == "@I1@": # Jerry Shane Sanderson
        if "children" not in p: p["children"] = []
        if "@I700@" not in p["children"]: p["children"].append("@I700@")
        if "@I701@" not in p["children"]: p["children"].append("@I701@")

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
