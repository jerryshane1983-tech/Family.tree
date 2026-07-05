import json

with open('sanderson_tree.json', 'r') as f:
    data = json.load(f)

people = {p['id']: p for p in data['people']}

def get_children(person_id):
    children_ids = set()
    person = people.get(person_id)
    if not person: return []
    if 'children' in person:
        for c in person['children']:
            children_ids.add(c)
    for pid, p in people.items():
        if 'parents' in p and person_id in p['parents']:
            children_ids.add(pid)
    return list(children_ids)

garland_id = next(pid for pid, p in people.items() if 'Garland' in p['name'])
kids_ids = get_children(garland_id)

print(f'Found {len(kids_ids)} children of Garland.')

cousins = []
for kid_id in kids_ids:
    kid = people[kid_id]
    kid_children_ids = get_children(kid_id)
    for cid in kid_children_ids:
        c = people[cid]
        cousins.append((c['name'], kid['name']))

print(f'Found {len(cousins)} cousins.')
for name, parent in cousins:
    print(f'- {name} (child of {parent})')
