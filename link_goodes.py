import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Define the children for each son
cj_children = ["@I850@", "@I451@", "@I452@"]
duffy_children = ["@I453@", "@I454@", "@I455@"]
miles_children = ["@I456@", "@I457@", "@I458@", "@I459@"]

# Apply them
for p in data["people"]:
    if p["id"] == "@I441@":
        p["spouse"] = "Suzanne"
        p["children"] = list(set(p.get("children", []) + cj_children))
    elif p["id"] == "@I442@":
        p["children"] = list(set(p.get("children", []) + duffy_children))
    elif p["id"] == "@I443@":
        p["spouse"] = "Jackie"
        p["children"] = list(set(p.get("children", []) + miles_children))

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Goode grandchildren all hooked up!")
