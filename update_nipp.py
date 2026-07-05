import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Add new people
new_people = [
    {
      "id": "@I420@",
      "name": "Lorene (Nipp) Montgomery",
      "gender": "F",
      "parents": ["@I70@", "@I71@"],
      "spouse": "Carroll Wayne Montgomery",
      "children": ["@I430@", "@I431@", "@I432@", "@I433@"],
      "note": "Resided in Marietta, OK."
    },
    {
      "id": "@I430@",
      "name": "Mark Montgomery",
      "gender": "M",
      "note": "2nd Cousin. Married Ali. Resides in Celina, TX."
    },
    {
      "id": "@I431@",
      "name": "Bronwyn Montgomery",
      "gender": "F",
      "note": "2nd Cousin. Married Jackie Carter. Resides in Marietta, OK."
    },
    {
      "id": "@I432@",
      "name": "Sheryl Lynn Montgomery",
      "gender": "F",
      "note": "2nd Cousin. Married Randall Harris. Preceded father in death."
    },
    {
      "id": "@I433@",
      "name": "Gregory Wayne Montgomery",
      "gender": "M",
      "note": "2nd Cousin. Married Sue. Preceded father in death."
    },
    {
      "id": "@I421@",
      "name": "Linda Sue (Nipp) Williams",
      "gender": "F",
      "parents": ["@I70@", "@I71@"],
      "spouse": "Warren Williams",
      "note": "Resided in Rubottom, OK."
    }
]

data["people"].extend(new_people)

# Update Jessie Pearl Powell's children
for p in data["people"]:
    if p["id"] == "@I70@":
        if "children" not in p:
            p["children"] = []
        if "@I420@" not in p["children"]: p["children"].append("@I420@")
        if "@I421@" not in p["children"]: p["children"].append("@I421@")

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
