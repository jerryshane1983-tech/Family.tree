import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add new people (Gen 1R)
new_people = [
    {
      "id": "@I500@",
      "name": "Billy Jack Drinnon",
      "gender": "M",
      "parents": ["@I22@"],
      "note": "1st Cousin 1R (Son of Rachel Hacker)."
    },
    {
      "id": "@I501@",
      "name": "Desiree Drinnon",
      "gender": "F",
      "parents": ["@I22@"],
      "note": "1st Cousin 1R (Daughter of Rachel Hacker)."
    },
    {
      "id": "@I502@",
      "name": "Brodey Canales",
      "gender": "M",
      "parents": ["@I24@"],
      "note": "1st Cousin 1R (Son of Lisa Hacker)."
    },
    {
      "id": "@I503@",
      "name": "Autumn Canales",
      "gender": "F",
      "parents": ["@I24@"],
      "note": "1st Cousin 1R (Daughter of Lisa Hacker)."
    },
    {
      "id": "@I504@",
      "name": "Jerry Wayne Hacker",
      "gender": "M",
      "parents": ["@I23@"],
      "note": "1st Cousin 1R (Son of Billy Don Hacker)."
    },
    {
      "id": "@I505@",
      "name": "Mason Salsbury",
      "gender": "M",
      "parents": ["@I21@"],
      "note": "1st Cousin 1R (Likely son of Mary Hacker)."
    },
    {
      "id": "@I506@",
      "name": "Summer (Hacker/Fisher)",
      "gender": "F",
      "parents": ["@I21@"],
      "note": "1st Cousin 1R (Likely daughter of Mary Hacker)."
    },
    {
      "id": "@I507@",
      "name": "Amber (Hacker/Fisher)",
      "gender": "F",
      "parents": ["@I21@"],
      "note": "1st Cousin 1R (Likely daughter of Mary Hacker)."
    },
    {
      "id": "@I508@",
      "name": "Katelynn (Hacker/Fisher)",
      "gender": "F",
      "parents": ["@I21@"],
      "note": "1st Cousin 1R (Likely daughter of Mary Hacker)."
    },
    {
      "id": "@I509@",
      "name": "Elizabeth (Hacker/Fisher)",
      "gender": "F",
      "parents": ["@I21@"],
      "note": "1st Cousin 1R (Likely daughter of Mary Hacker)."
    }
]

data["people"].extend(new_people)

# Update parents' children arrays
for p in data["people"]:
    if p["id"] == "@I22@": # Rachel Hacker
        p["children"] = ["@I500@", "@I501@"]
    elif p["id"] == "@I24@": # Lisa Hacker
        p["children"] = ["@I502@", "@I503@"]
    elif p["id"] == "@I23@": # Billy Don Hacker
        p["children"] = ["@I504@"]
    elif p["id"] == "@I21@": # Mary Hacker
        p["children"] = ["@I505@", "@I506@", "@I507@", "@I508@", "@I509@"]

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
