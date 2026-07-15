import json
import re

def main():
    tree_file = 'sanderson_tree.json'
    
    with open(tree_file, 'r') as f:
        data = json.load(f)
        
    people = data.get("people", [])
    
    # Find the highest ID to generate new ones
    max_id = 0
    for p in people:
        match = re.search(r'@I(\d+)@', p["id"])
        if match:
            num = int(match.group(1))
            if num > max_id:
                max_id = num

    def get_new_id():
        nonlocal max_id
        max_id += 1
        return f"@I{max_id}@"

    # Update spouses for Vernon children
    spouse_map = {
        "@I350@": "Betty Jane DeFoor (later Lois)",
        "@I351@": "Judy",
        "@I352@": "Kathryn",
        "@I353@": "Jeanne (companion: Lou Fincher)",
        "@I354@": "Clifford King",
        "@I355@": "James Hayes",
        "@I356@": "Danny Bray",
        "@I357@": "Jim Menke (later Billy Voyles)"
    }
    
    for p in people:
        if p["id"] in spouse_map:
            p["spouse"] = spouse_map[p["id"]]

    new_people = []
    
    # Helper to add a person
    def add_person(name, parents=None, spouse=None, note=None, death_year=None):
        pid = get_new_id()
        person = {"id": pid, "name": name, "gender": "U"}
        if parents:
            person["parents"] = parents
        if spouse:
            person["spouse"] = spouse
        if note:
            person["note"] = note
        if death_year:
            person["death_year"] = death_year
        new_people.append(person)
        
        # Link children to parents in the parent object
        if parents:
            for parent_id in parents:
                for p in people + new_people:
                    if p["id"] == parent_id:
                        if "children" not in p:
                            p["children"] = []
                        if pid not in p["children"]:
                            p["children"].append(pid)
        return pid

    # Carl 'Dean' Vernon's children (@I353@)
    carl_id = "@I353@"
    mindy_id = add_person("Mindy Robinson", parents=[carl_id], note="Identified from 2020 obituary.")
    greg_id = add_person("Greg Piper", parents=[carl_id], note="Identified from 2020 obituary.")
    dillon_id = add_person("Dillon Vernon", parents=[carl_id], note="Identified from 2020 obituary.")
    caleb_id = add_person("Caleb Vernon", parents=[carl_id], spouse="Mikayla", note="Identified from 2020 obituary.")
    candace_id = add_person("Candace Barella", parents=[carl_id], note="Identified from 2020 obituary.")

    # Connie Dianne (Vernon) King's children (@I354@)
    connie_id = "@I354@"
    bradley_id = add_person("Bradley Con King", parents=[connie_id], death_year=2014, note="Identified from 2016 obituary.")

    # Debbie (Vernon) Hayes' children (@I355@)
    debbie_id = "@I355@"
    chris_id = add_person("Chris Hayes", parents=[debbie_id], note="Deceased. Identified as nephew in Connie's 2016 obit.")

    # Carl's grandchildren (Great-grandchildren of Meady Mae)
    # We assign Robinson kids to Mindy Robinson. Others are assigned to Carl as grandchildren in notes since parents are ambiguous.
    cooper_id = add_person("Cooper Robinson", parents=[mindy_id], note="Grandson of Carl Dean Vernon.")
    parker_id = add_person("Parker Robinson", parents=[mindy_id], note="Grandson of Carl Dean Vernon.")
    
    # Ambiguous parentage (list without parents, just notes for now to keep tree clean)
    add_person("Corbin Dean Vernon", note="Grandson of Carl Dean Vernon (Parent ambiguous between Dillon/Caleb).")
    add_person("Camdyn Vernon", note="Grandchild of Carl Dean Vernon.")
    add_person("Landree Vernon", note="Grandchild of Carl Dean Vernon.")
    add_person("Chase Vernon", note="Grandchild of Carl Dean Vernon.")
    add_person("Raelyn Mitchell", note="Grandchild of Carl Dean Vernon.")
    add_person("Raylynn Buechner", note="Grandchild of Carl Dean Vernon.")
    add_person("Donivon Buechner", note="Grandchild of Carl Dean Vernon.")
    add_person("Jenelle Buechner", note="Grandchild of Carl Dean Vernon.")
    
    # Michael Tanner Vernon
    add_person("Michael Tanner Vernon", note="Great-grandson of Melvin 'Smooth' and Meady Mae Vernon. Grandfather was Jimmie Jo Mann.", death_year=2021)

    people.extend(new_people)
    
    with open(tree_file, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully added {len(new_people)} new descendants and updated spouses!")

if __name__ == "__main__":
    main()
