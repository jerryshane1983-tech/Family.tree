import json
import re

with open('sanderson_tree.json', 'r') as f:
    data = json.load(f)

people = data.get("people", [])
print(f"Total people in JSON: {len(people)}")

# Let's check how many people have names, IDs
missing_names = [p for p in people if not p.get("name")]
missing_ids = [p for p in people if not p.get("id")]
print(f"Missing names: {len(missing_names)}")
print(f"Missing IDs: {len(missing_ids)}")

# Let's check for dates
has_birth_date = [p for p in people if p.get("birth_date")]
has_birth_year = [p for p in people if p.get("birth_year")]
has_death_date = [p for p in people if p.get("death_date")]
has_death_year = [p for p in people if p.get("death_year")]
print(f"Has birth_date: {len(has_birth_date)}")
print(f"Has birth_year: {len(has_birth_year)}")
print(f"Has death_date: {len(has_death_date)}")
print(f"Has death_year: {len(has_death_year)}")

with open('family_tree.html', 'r') as f:
    html = f.read()

# Extract all IDs mentioned in HTML treeData
html_ids = re.findall(r'"id": "(@I\d+@)"', html)
html_ids = set(html_ids)
print(f"Unique IDs in HTML: {len(html_ids)}")

# Check if any ID from HTML is missing in JSON
json_ids = {p.get("id") for p in people}
missing_from_json = html_ids - json_ids
print(f"IDs in HTML but missing in JSON: {missing_from_json}")

# Check if names match for the overlapping IDs
print("\nChecking for missing dates that exist in HTML:")
html_name_date = re.findall(r'"name": "([^"]+ \(.*?\))"', html)
html_dates_map = {}
for match in html_name_date:
    # Example: "Robert Powell (1845-?)"
    m = re.search(r'(.+) \(([\d\?]+)-([\d\?]+)\)', match)
    if m:
        name = m.group(1).strip()
        b = m.group(2)
        d = m.group(3)
        html_dates_map[name] = (b, d)

for p in people:
    name = p.get('name', '').replace('[Pedigree Collapse: ', '').replace(']', '')
    # handle names like "Jessie Pearl Powell [TARGET]"
    name = name.replace(' [TARGET]', '')
    
    if name in html_dates_map:
        b_html, d_html = html_dates_map[name]
        b_json = p.get('birth_year') or (p.get('birth_date') or '').split('-')[0] or '?'
        d_json = p.get('death_year') or (p.get('death_date') or '').split('-')[0] or '?'
        
        b_json = str(b_json)
        d_json = str(d_json)
        
        issues = []
        if b_html != '?' and b_html != b_json:
            issues.append(f"Birth: HTML={b_html}, JSON={b_json}")
        if d_html != '?' and d_html != d_json:
            issues.append(f"Death: HTML={d_html}, JSON={d_json}")
            
        if issues:
            print(f"Mismatch for {name}: {', '.join(issues)}")

