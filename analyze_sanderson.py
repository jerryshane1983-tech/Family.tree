import json
import networkx as nx

def analyze_genealogy(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Initialize a directed graph
    G = nx.DiGraph()

    # Map IDs to names for better visualization/reporting
    id_to_name = {}
    for person in data['people']:
        person_id = person['id']
        name = person.get('name', person_id)
        id_to_name[person_id] = name
        
        # Add node with attributes
        G.add_node(person_id, name=name, gender=person.get('gender'))

    # Add edges for parent-child relationships
    for person in data['people']:
        person_id = person['id']
        
        # From parents list
        parents = person.get('parents', [])
        for parent_id in parents:
            if parent_id in id_to_name:
                G.add_edge(parent_id, person_id, relationship='parent-child')
        
        # From children list (if exists)
        children = person.get('children', [])
        for child_id in children:
            if child_id in id_to_name:
                G.add_edge(person_id, child_id, relationship='parent-child')

    # Basic analysis
    print(f"Network Analysis of Sanderson Family Tree:")
    print(f"------------------------------------------")
    print(f"Total People (Nodes): {G.number_of_nodes()}")
    print(f"Total Relationships (Edges): {G.number_of_edges()}")
    
    # Identify roots (people with no parents in the dataset)
    roots = [n for n, d in G.in_degree() if d == 0]
    print(f"\nAncestral Roots (No parents listed):")
    for root in roots:
        print(f" - {id_to_name[root]} ({root})")

    # Identify "leaf" nodes (people with no children in the dataset)
    leaves = [n for n, d in G.out_degree() if d == 0]
    print(f"\nDescendant Leaves (No children listed):")
    # Limiting output to first 5 for brevity
    for leaf in leaves[:5]:
        print(f" - {id_to_name[leaf]} ({leaf})")
    if len(leaves) > 5:
        print(f" ... and {len(leaves) - 5} more.")

    # Find the longest lineage (longest path)
    try:
        longest_path = nx.dag_longest_path(G)
        print(f"\nLongest Lineage Path ({len(longest_path)} generations):")
        for i, person_id in enumerate(longest_path):
            print(f" {i+1}. {id_to_name[person_id]}")
    except nx.NetworkXUnfeasible:
        print("\nCycle detected in graph! (Not a pure tree)")

    # Sibling Detection
    print(f"\nSibling Group Detection:")
    
    # 1. Infer relationships to build a complete parent-child map
    # mapping: child_id -> set of parent_ids
    child_to_parents = {}
    for person in data['people']:
        child_id = person['id']
        parents = set(person.get('parents', []))
        if child_id not in child_to_parents:
            child_to_parents[child_id] = set()
        child_to_parents[child_id].update(parents)
        
        # From 'children' list on parent node
        for c_id in person.get('children', []):
            if c_id not in child_to_parents:
                child_to_parents[c_id] = set()
            child_to_parents[c_id].add(child_id)

    # 2. Group by shared parent sets
    parent_sets = {}
    for child_id, parents in child_to_parents.items():
        if parents:
            parent_tuple = tuple(sorted(list(parents)))
            if parent_tuple not in parent_sets:
                parent_sets[parent_tuple] = set()
            parent_sets[parent_tuple].add(child_id)

    # 3. Handle explicit 'siblings' field (Disjoint Set Union style)
    # Using a simple list of sets for now
    explicit_groups = []
    for person in data['people']:
        p_id = person['id']
        sibs = person.get('siblings', [])
        if sibs:
            group = set([p_id] + sibs)
            # Merge with existing groups if they overlap
            merged = False
            for existing in explicit_groups:
                if not existing.isdisjoint(group):
                    existing.update(group)
                    merged = True
                    break
            if not merged:
                explicit_groups.append(group)

    # Output consolidated groups
    consolidated_final = []
    # Merge all groups that have any overlap
    all_raw_groups = [children for children in parent_sets.values() if len(children) > 1] + explicit_groups
    
    while all_raw_groups:
        current = all_raw_groups.pop(0)
        merged = False
        for i, other in enumerate(consolidated_final):
            if not current.isdisjoint(other):
                consolidated_final[i].update(current)
                merged = True
                break
        if not merged:
            consolidated_final.append(current)

    if consolidated_final:
        for group in consolidated_final:
            # Try to find parents for this group
            # We look for any child in the group who has parents listed
            group_parents = set()
            for member_id in group:
                group_parents.update(child_to_parents.get(member_id, set()))
            
            child_names = ", ".join([id_to_name.get(c, c) for c in sorted(list(group))])
            
            if group_parents:
                parent_names = " & ".join([id_to_name.get(p, p) for p in sorted(list(group_parents))])
                print(f" - Children of {parent_names}: {child_names}")
            else:
                print(f" - Sibling group (parents unknown): {child_names}")
    else:
        print(" - No sibling groups detected.")

    # Compute Centrality (who is most 'central' to the connectivity)
    degree_cent = nx.degree_centrality(G)
    # Sort and get top 3
    top_central = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"\nMost Connected Individuals (Degree Centrality):")
    for person_id, score in top_central:
        print(f" - {id_to_name[person_id]}: {score:.3f}")

if __name__ == "__main__":
    analyze_genealogy('sanderson_tree.json')
