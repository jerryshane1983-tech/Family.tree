import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

for p in data["people"]:
    # Remove Katelynn (@I508@) and Elizabeth (@I509@) from Mary (@I21@)
    if p["id"] == "@I21@":
        if "children" in p:
            if "@I508@" in p["children"]: p["children"].remove("@I508@")
            if "@I509@" in p["children"]: p["children"].remove("@I509@")
    
    # Add Katelynn to Billy Don (@I23@)
    elif p["id"] == "@I23@":
        if "children" not in p:
            p["children"] = []
        if "@I508@" not in p["children"]: 
            p["children"].append("@I508@")
        
    # Add Elizabeth to Lisa (@I24@)
    elif p["id"] == "@I24@":
        if "children" not in p:
            p["children"] = []
        if "@I509@" not in p["children"]: 
            p["children"].append("@I509@")
        
    # Update Katelynn's parents and notes
    elif p["id"] == "@I508@":
        p["parents"] = ["@I23@"]
        p["note"] = "1st Cousin 1R (Daughter of Billy Don Hacker)."
        p["name"] = "Katelynn Hacker"
        
    # Update Elizabeth's parents and notes
    elif p["id"] == "@I509@":
        p["parents"] = ["@I24@"]
        p["note"] = "1st Cousin 1R (Daughter of Lisa Hacker)."
        p["name"] = "Elizabeth"

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)
