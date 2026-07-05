import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

for p in data["people"]:
    if p["id"] == "@I21@": # Mary
        if "@I505@" in p.get("children", []):
            p["children"].remove("@I505@")
    elif p["id"] == "@I23@": # Billy Don
        if "children" not in p:
            p["children"] = []
        if "@I505@" not in p["children"]:
            p["children"].append("@I505@")
    elif p["id"] == "@I505@": # Mason
        p["parents"] = ["@I23@"]
        p["note"] = "1st Cousin 1R (Son of Billy Don Hacker)."

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
