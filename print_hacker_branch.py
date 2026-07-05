import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

people = {p["id"]: p for p in data["people"]}

def print_branch(person_id, indent=0):
    p = people.get(person_id)
    if not p: return
    
    prefix = "  " * indent + "- "
    note = f" ({p.get('note', '')})" if 'note' in p else ""
    spouse = f" [Spouse/Partner: {p.get('spouse', 'Unknown')}]" if 'spouse' in p else ""
    
    # Handle implicit spouses mentioned in notes for this specific printout
    if not spouse and 'note' in p and 'Partner:' in p['note']:
        partner_str = p['note'].split('Partner: ')[1].split('.')[0]
        spouse = f" [Partner: {partner_str}]"
    
    # Clean up note for display if we extracted partner
    display_note = note
    if 'Partner:' in note:
        display_note = f" ({note.split('. Partner:')[0].replace(' (', '')})"

    print(f"{prefix}{p['name']}{spouse}{display_note}")
    
    for child_id in p.get("children", []):
        print_branch(child_id, indent + 1)

print("### The Hacker Branch (Descendants of Judy Powell & Billy Floyd Hacker)\n")
print_branch("@I14@")
