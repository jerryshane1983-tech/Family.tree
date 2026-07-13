import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# First, fix Raymond Lee Self (@I435@)
for p in data["people"]:
    if p["id"] == "@I435@" and p["name"] == "Raymond Lee Self":
        if "spouse" in p:
            del p["spouse"]
        if "children" in p:
            del p["children"]
        if "note" in p:
            p["note"] = "Husband of Oleta Pearl Nipp."
        break

# Change Justin Nipp's ID from @I435@ to @I900@
for p in data["people"]:
    if p["name"] == "Justin Nipp":
        p["id"] = "@I900@"
        p["spouse"] = "Kilby"
        p["children"] = ["@I435_1@", "@I435_2@"]
        p["note"] = "Owns/operated Wayne Wood Agency. (Note: May legally be Curtiss Justin Nipp, based on 2025 news reports mentioning a Curtiss and Kilby Nipp at this agency)."
        break

# Update Curtiss Nipp to point to @I900@ instead of @I435@
for p in data["people"]:
    if p["id"] == "@I427@":  # Curtiss
        if "@I435@" in p.get("children", []):
            p["children"].remove("@I435@")
            p["children"].append("@I900@")
        break

# Update Morgan and Cannon's parents to @I900@
for p in data["people"]:
    if p["id"] in ["@I435_1@", "@I435_2@"]:
        if "@I435@" in p.get("parents", []):
            p["parents"].remove("@I435@")
            p["parents"].append("@I900@")

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Collision Fixed!")
