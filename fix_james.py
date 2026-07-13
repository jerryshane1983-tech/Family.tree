import json

file_path = "sanderson_tree.json"

with open(file_path, 'r') as f:
    data = json.load(f)

# Update Nadine (@I422@) - add @I440@ back to children
for p in data["people"]:
    if p["id"] == "@I422@":
        if "@I440@" not in p.get("children", []):
            p["children"].append("@I440@")
        break

# Update CJ (@I441@) - remove @I440@ and add @I850@ to children
for p in data["people"]:
    if p["id"] == "@I441@":
        if "@I440@" in p.get("children", []):
            p["children"].remove("@I440@")
        if "@I850@" not in p.get("children", []):
            p.setdefault("children", []).append("@I850@")
        break

# Update James the brother (@I440@)
for p in data["people"]:
    if p["id"] == "@I440@":
        p["parents"] = ["@I422@"]
        p["note"] = "Child of A.J. Goode and Nadine. Brother of C.J., Duffy, and Miles. Died in a car wreck, preceding parents in death (1979)."
        break

# Add James the son (@I850@)
new_james = {
    "id": "@I850@",
    "name": "James Goode",
    "gender": "M",
    "parents": ["@I441@"],
    "note": "Child of C.J. Goode and Suzanne. Named after his late uncle James."
}
data["people"].append(new_james)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed the two James Goodes!")
