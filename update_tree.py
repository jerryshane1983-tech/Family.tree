import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Update Andy Nipp
for p in data["people"]:
    if p["id"] == "@I310@":
        p["children"] = ["@I310_1@", "@I310_2@"]
        p["death_year"] = 2020
        p["birth_year"] = 1967
        p["note"] = "Passed away April 13, 2020. Worked in telephone towers and oil field service. Enjoyed 4-wheelers and mechanics."

# Update Quintin Nipp
for p in data["people"]:
    if p["id"] == "@I311@":
        p["children"] = ["@I311_1@", "@I311_2@", "@I311_3@"]

# Add new people
new_people = [
    {
        "id": "@I310_1@",
        "name": "Andrea (Nipp) Hartwell",
        "gender": "F",
        "parents": ["@I310@"],
        "spouse": "Justin Hartwell"
    },
    {
        "id": "@I310_2@",
        "name": "Andrew Nipp",
        "gender": "M",
        "parents": ["@I310@"]
    },
    {
        "id": "@I311_1@",
        "name": "Cheyenne Nipp",
        "gender": "F",
        "parents": ["@I311@"]
    },
    {
        "id": "@I311_2@",
        "name": "Cassidy Nipp",
        "gender": "F",
        "parents": ["@I311@"]
    },
    {
        "id": "@I311_3@",
        "name": "Chelsey Nipp",
        "gender": "F",
        "parents": ["@I311@"]
    }
]

data["people"].extend(new_people)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Updated!")
