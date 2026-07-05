import json
import collections

def analyze_tree():
    with open('/data/data/com.termux/files/home/sanderson_tree.json', 'r') as f:
        data = json.load(f)
        
    people = data if isinstance(data, list) else data.get('people', [])

    # Basic stats
    total_people = len(people)
    
    # Holes analysis
    missing_birth = []
    missing_death = []
    missing_parents = []
    
    # Duplicate analysis
    names_count = collections.defaultdict(list)
    
    for p in people:
        name = p.get('name', 'Unknown')
        id_str = p.get('id', 'No ID')
        
        # Check for duplicates
        if name != 'Unknown' and not name.startswith('[Pedigree'):
            names_count[name].append(id_str)
            
        # Check for missing data
        birth_year = p.get('birth_year') or p.get('birth_date')
        death_year = p.get('death_year') or p.get('death_date')
        parents = p.get('parents', [])
        
        # Some people are marked with "?-?" in name or just lack fields
        if not birth_year and '?' not in name:
            missing_birth.append(name)
        if not parents:
            missing_parents.append(name)

    # Output Markdown report
    with open('/data/data/com.termux/files/home/.gemini/antigravity-cli/brain/cae6278d-ad7b-4185-b664-e426281c8fb7/family_tree_audit.md', 'w') as out:
        out.write("# 🌳 Family Tree Data Audit & Research Checklist\n\n")
        out.write(f"**Total profiles analyzed:** {total_people}\n\n")
        
        out.write("## 1. Potential Duplicates\n")
        out.write("These names appear multiple times and might need to be merged:\n")
        dupes = {name: ids for name, ids in names_count.items() if len(ids) > 1}
        if dupes:
            for name, ids in dupes.items():
                out.write(f"- **{name}** (IDs: {', '.join(ids)})\n")
        else:
            out.write("- *No exact duplicate names found.*\n")
            
        out.write("\n## 2. Missing Birth Dates (Top 15)\n")
        out.write("Finding birth dates helps anchor these people in history:\n")
        for name in missing_birth[:15]:
            out.write(f"- [ ] {name}\n")
            
        out.write("\n## 3. Missing Parents (Dead Ends) (Top 15)\n")
        out.write("These people represent the furthest back we've gone on their branches. Finding their parents will break down brick walls:\n")
        for name in missing_parents[:15]:
            out.write(f"- [ ] {name}\n")
            
    print("Report generated successfully!")

if __name__ == '__main__':
    analyze_tree()
