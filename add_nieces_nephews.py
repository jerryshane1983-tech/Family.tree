import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add new people (Gen 1R - Nieces/Nephews)
new_people = [
    # Jennifer's children
    {"id": "@I800@", "name": "Braidyn Beyer", "gender": "M", "parents": ["@I12@"], "note": "Nephew (Son of Jennifer Beyer)."},
    {"id": "@I801@", "name": "Garrett Beyer", "gender": "M", "parents": ["@I12@"], "note": "Nephew (Son of Jennifer Beyer)."},
    {"id": "@I802@", "name": "Lillee Beyer", "gender": "F", "parents": ["@I12@"], "note": "Niece (Daughter of Jennifer Beyer)."},
    # Stephanie's children
    {"id": "@I803@", "name": "Elisabeth VanCuren", "gender": "F", "parents": ["@I13@"], "note": "Niece (Daughter of Stephanie VanCuren)."},
    {"id": "@I804@", "name": "Aaron VanCuren", "gender": "M", "parents": ["@I13@"], "note": "Nephew (Son of Stephanie VanCuren)."},
    # Donnie's children
    {"id": "@I805@", "name": "Ashlynn Hogan", "gender": "F", "parents": ["@I11@"], "note": "Niece (Daughter of Donnie Hogan)."},
    {"id": "@I806@", "name": "Cole Keith Hogan", "gender": "M", "parents": ["@I11@"], "note": "Nephew (Son of Donnie Hogan)."},
    # Randall's child
    {"id": "@I807@", "name": "Kaitlyn Sanderson", "gender": "F", "parents": ["@I10@"], "note": "Niece (Daughter of Randall Sanderson)."}
]

data["people"].extend(new_people)

# Update siblings' children arrays
for p in data["people"]:
    if p["id"] == "@I12@": # Jennifer
        p["children"] = ["@I800@", "@I801@", "@I802@"]
        p["spouse"] = "Jodie Beyer"
    elif p["id"] == "@I13@": # Stephanie
        p["children"] = ["@I803@", "@I804@"]
        p["spouse"] = "Erik VanCuren"
    elif p["id"] == "@I11@": # Donnie
        p["children"] = ["@I805@", "@I806@"]
    elif p["id"] == "@I10@": # Randall
        p["children"] = ["@I807@"]

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
