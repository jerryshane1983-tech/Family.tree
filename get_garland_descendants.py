import json

def get_descendants(person_id, tree_data, depth=0, visited=None):
    if visited is None:
        visited = set()
    if person_id in visited:
        return ""
    visited.add(person_id)
    
    person = tree_data.get(person_id)
    if not person:
        return ""
    
    indent = "  " * depth
    name = person.get("name", "Unknown")
    birth = person.get("birth_year", "?")
    death = person.get("death_year", "?")
    if birth == "?" and death == "?":
        dates = ""
    else:
        dates = f" ({birth} - {death})"
    
    spouse = person.get("spouse")
    spouse_str = f" [Spouse: {spouse}]" if spouse else ""
    
    result = f"{indent}- {name}{dates}{spouse_str} ({person_id})\n"
    
    # Sort children to keep output consistent (optional, but good)
    children = sorted(list(set(person.get("all_children", []))))
    for child_id in children:
        result += get_descendants(child_id, tree_data, depth + 1, visited)
        
    return result

with open('sanderson_tree.json', 'r') as f:
    data = json.load(f)

tree_dict = {}
for p in data["people"]:
    p["all_children"] = set(p.get("children", []))
    tree_dict[p["id"]] = p

# Link parents -> children if child explicitly lists parents
for p in data["people"]:
    for parent_id in p.get("parents", []):
        if parent_id in tree_dict:
            tree_dict[parent_id]["all_children"].add(p["id"])

print(get_descendants("@I4@", tree_dict))
