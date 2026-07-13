import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Update Justin Nipp (@I435@)
for p in data["people"]:
    if p["id"] == "@I435@":
        p["spouse"] = "Kilby"
        p["children"] = ["@I435_1@", "@I435_2@"]
        p["note"] = "Owns/operated Wayne Wood Agency. (Note: May legally be Curtiss Justin Nipp, based on 2025 news reports mentioning a Curtiss and Kilby Nipp at this agency)."
        break

# Update Travis Nipp (@I436@)
for p in data["people"]:
    if p["id"] == "@I436@":
        p["spouse"] = "Audrey"
        p["children"] = ["@I436_1@"]
        p["note"] = "Employed as a Security Safety Health and Environmental Supervisor with Exxon Mobil."
        break

# Add grandchildren
new_people = [
    {
        "id": "@I435_1@",
        "name": "Morgan Nipp",
        "gender": "F",
        "parents": ["@I435@"],
        "note": "Attended Oklahoma State University (Biochemistry and Molecular Biology)."
    },
    {
        "id": "@I435_2@",
        "name": "Cannon Nipp",
        "gender": "M",
        "parents": ["@I435@"]
    },
    {
        "id": "@I436_1@",
        "name": "Addilyn 'Addi' Nipp",
        "gender": "F",
        "parents": ["@I436@"]
    }
]

data["people"].extend(new_people)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Updated grandchildren!")
