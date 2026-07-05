import json

def merge_duplicates():
    input_file = '/data/data/com.termux/files/home/sanderson_tree.json'
    
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    people = data['people']
    
    # Pairs to merge: {secondary_id: primary_id}
    merge_map = {
        "@I365@": "@I420@", # Claud William Nipp
        "@I814@": "@I421@", # Ida Dorleen Nipp
        "@I366@": "@I423@", # Oleta Pearl (Nipp) Self
        "@I808@": "@I424@", # Lorene (Nipp) Montgomery
        "@I809@": "@I425@", # Linda Sue (Nipp) Williams
        "@I367@": "@I426@", # Donnie Nipp
        "@I369@": "@I427@"  # Curtiss Nipp
    }
    
    # We will build a new list of people, omitting the secondaries.
    # Before omitting, we should grab any data they have that the primary lacks.
    
    person_dict = {p['id']: p for p in people}
    
    for sec_id, prim_id in merge_map.items():
        if sec_id in person_dict and prim_id in person_dict:
            sec_p = person_dict[sec_id]
            prim_p = person_dict[prim_id]
            
            # Merge fields (if primary is missing something secondary has)
            for key, val in sec_p.items():
                if key not in prim_p or not prim_p[key]:
                    prim_p[key] = val
                    
            # We don't merge arrays blindly to avoid duplicating existing links, 
            # but we update the global references next.

    # Now we remove secondaries
    new_people = [p for p in people if p['id'] not in merge_map]
    
    # Update references in all remaining people
    def update_refs(id_list):
        if not id_list: return id_list
        if isinstance(id_list, str):
            return merge_map.get(id_list, id_list)
        return list(set(merge_map.get(i, i) for i in id_list))
    
    for p in new_people:
        for ref_key in ['parents', 'siblings', 'children']:
            if ref_key in p:
                p[ref_key] = update_refs(p[ref_key])
        if 'spouse' in p:
            p['spouse'] = update_refs(p['spouse'])
            
    data['people'] = new_people
    
    with open(input_file, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully merged {len(merge_map)} duplicate pairs!")

if __name__ == '__main__':
    merge_duplicates()
