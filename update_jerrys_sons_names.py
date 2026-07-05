import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

for p in data["people"]:
    if p["id"] == "@I603@":
        p["name"] = "Ruger Wayne Hacker"
    elif p["id"] == "@I604@":
        p["name"] = "Ryker Blaine Hacker"

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
