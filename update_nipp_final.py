import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add new people
new_people = [
    {
      "id": "@I365@",
      "name": "Claud William Nipp",
      "gender": "M",
      "birth_year": 1930,
      "death_year": 1990,
      "parents": ["@I70@", "@I71@"],
      "note": "Buried at Simon Cemetery, Love Co, OK."
    },
    {
      "id": "@I366@",
      "name": "Oleta Pearl (Nipp) Self",
      "gender": "F",
      "birth_year": 1941,
      "death_year": 2010,
      "parents": ["@I70@", "@I71@"],
      "spouse": "Raymond Lee Self",
      "note": "Buried at Jimtown Cemetery, Love Co, OK."
    },
    {
      "id": "@I367@",
      "name": "Donnie Nipp",
      "gender": "M",
      "parents": ["@I70@", "@I71@"],
      "spouse": "Jeannie",
      "note": "Resided in Wilson, OK."
    },
    {
      "id": "@I368@",
      "name": "Raddie Nadine (Nipp) Goode",
      "gender": "F",
      "birth_year": 1939,
      "parents": ["@I70@", "@I71@"],
      "spouse": "A.J. Goode",
      "children": ["@I440@", "@I441@", "@I442@", "@I443@"],
      "note": "Resided in Wilson, OK."
    },
    {
      "id": "@I440@",
      "name": "James Goode",
      "gender": "M",
      "note": "2nd Cousin. Preceded parents in death (1979)."
    },
    {
      "id": "@I441@",
      "name": "C.J. Goode",
      "gender": "M",
      "note": "2nd Cousin. Married Suzanne."
    },
    {
      "id": "@I442@",
      "name": "Duffy Goode",
      "gender": "M",
      "note": "2nd Cousin."
    },
    {
      "id": "@I443@",
      "name": "Miles Goode",
      "gender": "M",
      "note": "2nd Cousin. Married Jackie."
    },
    {
      "id": "@I369@",
      "name": "Curtiss Nipp",
      "gender": "M",
      "parents": ["@I70@", "@I71@"],
      "spouse": "Brenda",
      "note": "Resided in Simon, OK."
    },
    {
      "id": "@I422@",
      "name": "Ida Dorleen Nipp",
      "gender": "F",
      "birth_year": 1936,
      "death_year": 1936,
      "parents": ["@I70@", "@I71@"],
      "note": "Died in infancy."
    }
]

data["people"].extend(new_people)

# Update Jessie Pearl Powell's children
for p in data["people"]:
    if p["id"] == "@I70@":
        if "children" not in p:
            p["children"] = []
        for child_id in ["@I365@", "@I366@", "@I367@", "@I368@", "@I369@", "@I422@"]:
            if child_id not in p["children"]: p["children"].append(child_id)

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
