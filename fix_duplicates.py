import json

with open('sanderson_tree.json', 'r') as f:
    data = json.load(f)

people = data['people']
max_id = max(int(p['id'].replace('@I', '').replace('@', '')) for p in people)

# Keep the first occurrence of an ID, reassign the rest
seen_ids = set()
reassigned = []

for p in people:
    pid = p['id']
    if pid in seen_ids:
        # Give it a new ID
        max_id += 1
        new_id = f"@I{max_id}@"
        print(f"Reassigning {p['name']} from {pid} to {new_id}")
        p['old_id'] = pid # temporary
        p['id'] = new_id
        reassigned.append(p)
    else:
        seen_ids.add(pid)

# Now we have to fix references.
# We have specific knowledge of the data:
# Claud William Nipp is the original @I420@. Lorene became the new @I420@ -> @I...
# We will fix the parent/child/spouse relationships manually here based on the names.

def get_id(name):
    for p in people:
        if name in p['name']:
            return p['id']
    return None

def set_children(parent_name, children_names):
    parent_id = get_id(parent_name)
    if not parent_id: return
    p_obj = next(p for p in people if p['id'] == parent_id)
    child_ids = []
    for c_name in children_names:
        cid = get_id(c_name)
        if cid:
            child_ids.append(cid)
            # set parent ref
            c_obj = next(c for c in people if c['id'] == cid)
            if 'parents' not in c_obj: c_obj['parents'] = []
            if parent_id not in c_obj['parents']:
                c_obj['parents'].append(parent_id)
    p_obj['children'] = child_ids

# Clean up ALL children/parents arrays that contain the duplicated IDs and let's rebuild them for these specific families.
for p in people:
    if 'old_id' in p:
        del p['old_id']
    
# Rebuild Claud William Nipp's children
set_children("Claud William Nipp", ["Claud William Nipp Jr.", "Terry (Nipp) Smith"])

# Rebuild Lorene (Nipp) Montgomery's children
set_children("Lorene (Nipp) Montgomery", ["Mark Montgomery", "Bronwyn Montgomery", "Sheryl Lynn Montgomery", "Gregory Wayne Montgomery", "James Montgomery"])

# Rebuild Linda Sue (Nipp) Williams's children
set_children("Linda Sue (Nipp) Williams", ["Amanda Williams"])

# Rebuild Raddie Nadine's children
set_children("Raddie Nadine (Nipp) Goode", ["C.J. Goode", "Duffy Goode", "Miles Goode", "James Goode (d. 2018)", "James Goode"]) 
# Wait, A.J. Goode is the spouse of Raddie. C.J, Duffy, Miles, and James Goode (d. 2018) are their children.
# Wait, there are TWO James Goodes. Let's find the one that died in 2018. Wait, earlier we couldn't find "James Goode (d. 2018)".
# Let's see all James Goodes.
jgs = [p for p in people if 'James Goode' in p['name']]
for jg in jgs:
    print("Found JG:", jg['name'], jg.get('note', ''))

# Fix A.J. Goode as spouse
aj = get_id("A.J. Goode")
raddie = get_id("Raddie Nadine")
if aj and raddie:
    next(p for p in people if p['id'] == raddie)['spouse'] = aj

# Ensure C.J. Goode children
set_children("C.J. Goode", ["Brock Goode", "Cullen Goode"])
# one of the James Goodes is child of C.J.
cj_jg = next((p['id'] for p in jgs if 'C.J. Goode' in p.get('note', '')), None)
if cj_jg:
    cj_obj = next(p for p in people if p['id'] == get_id("C.J. Goode"))
    if 'children' not in cj_obj: cj_obj['children'] = []
    if cj_jg not in cj_obj['children']: cj_obj['children'].append(cj_jg)

with open('sanderson_tree_fixed.json', 'w') as f:
    json.dump(data, f, indent=2)

