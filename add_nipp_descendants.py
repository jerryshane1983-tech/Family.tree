import json
import re

def get_max_id(data):
    max_id = 0
    for p in data.get('people', []):
        match = re.search(r'@I(\d+)@', p['id'])
        if match:
            num = int(match.group(1))
            if num > max_id:
                max_id = num
    return max_id

def main():
    file_path = "sanderson_tree.json"
    with open(file_path, "r") as f:
        data = json.load(f)

    max_id = get_max_id(data)
    next_id = max_id + 1

    def gen_id():
        nonlocal next_id
        new_id = f"@I{next_id}@"
        next_id += 1
        return new_id

    # Lookup map
    people_map = {p['id']: p for p in data['people']}

    def add_person(name, notes=None, parents=None, spouses=None, birth=None, death=None):
        pid = gen_id()
        person = {
            "id": pid,
            "name": name,
            "gender": "Unknown",
            "parents": parents or [],
            "children": [],
            "spouses": spouses or [],
            "birth_date": birth or "",
            "death_date": death or "",
            "notes": notes or ""
        }
        data['people'].append(person)
        people_map[pid] = person
        
        # Link children to parents
        for parent_id in (parents or []):
            if parent_id in people_map:
                if 'children' not in people_map[parent_id]:
                    people_map[parent_id]['children'] = []
                if pid not in people_map[parent_id]['children']:
                    people_map[parent_id]['children'].append(pid)
                    
        # Link spouses
        for spouse_id in (spouses or []):
            if spouse_id in people_map:
                if 'spouses' not in people_map[spouse_id]:
                    people_map[spouse_id]['spouses'] = []
                if pid not in people_map[spouse_id]['spouses']:
                    people_map[spouse_id]['spouses'].append(pid)
                    
        return pid

    # 1. Charles Floyd Nipp (@I361@)
    leona_id = add_person("Leona GeorgeAnn Chisum", birth="1934", death="2017", spouses=["@I361@"])
    bobby_id = add_person("Bobby Wayne Nipp", birth="1955", death="2005", parents=["@I361@", leona_id], notes="Passed away in a motorcycle accident.")
    brenda_id = add_person("Brenda Lee Wright", spouses=[bobby_id])
    add_person("Brandon Wayne Nipp", parents=[bobby_id, brenda_id])
    add_person("Dakota Andrew Nipp", parents=[bobby_id, brenda_id])
    add_person("MaKayla Rose Nipp", parents=[bobby_id, brenda_id])
    add_person("Johnny Nipp", parents=[bobby_id, brenda_id])
    add_person("Melanie (Nipp) Martin", parents=[bobby_id, brenda_id])

    # 2. Eric "Clay" Nipp (@I390@)
    erica_id = add_person("Erica Nipp", parents=["@I390@"])
    kyle_id = add_person("Kyle Nipp", parents=["@I390@"])
    caly_id = add_person("Caly (Nipp) Haynes", parents=["@I390@"])
    
    # Caly's children
    add_person("Jayke Haynes", parents=[caly_id])
    add_person("Maddyn Haynes", parents=[caly_id])
    add_person("Kynslei Haynes", parents=[caly_id])

    # 3. Lorene (Nipp) Montgomery (@I424@)
    # We will attach grandchildren directly to Lorene with a note because the exact parent is unconfirmed.
    sam_id = add_person("Sam Harris", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed from obituary.")
    jessica_id = add_person("Jessica (Montgomery/Harris?) Johnson", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed.")
    kelsi_id = add_person("Kelsi (Montgomery/Harris?) Flugum", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed.")
    mathilde_id = add_person("Mathilde Montgomery", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed.")
    kate_id = add_person("Kate Schmiege", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed.")
    gust_id = add_person("Gust Schmiege", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed.")
    josh_id = add_person("Josh Yates", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed.")
    cameron_id = add_person("Cameron Yates", parents=["@I424@"], notes="Grandchild of Lorene Nipp. Exact parent unconfirmed.")

    # Great-grandchildren attached to their respective parents
    add_person("Garrett Johnson", parents=[jessica_id])
    add_person("Kaylynn Johnson", parents=[jessica_id])
    add_person("Emma Flugum", parents=[kelsi_id])
    add_person("Zoey Flugum", parents=[kelsi_id])
    add_person("Kai Flugum", parents=[kelsi_id])

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully added new Nipp descendants. New max ID is {next_id - 1}.")

if __name__ == "__main__":
    main()
