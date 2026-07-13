import json
import os
import argparse
from google import genai

def load_tree(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def get_person_by_name_or_id(tree_data, query):
    for person in tree_data.get('people', []):
        if person.get('id') == query or person.get('name', '').lower() == query.lower():
            return person
    return None

def get_person_by_id(tree_data, pid):
    for person in tree_data.get('people', []):
        if person.get('id') == pid:
            return person
    return None

def format_person_details(person, tree_data):
    details = f"Name: {person.get('name', 'Unknown')}\n"
    if 'birth_date' in person:
        details += f"Birth Date: {person['birth_date']}\n"
    if 'birth_place' in person:
        details += f"Birth Place: {person['birth_place']}\n"
    
    # Get parents
    parents = []
    for pid in person.get('parents', []):
        p = get_person_by_id(tree_data, pid)
        if p: parents.append(p.get('name'))
    if parents:
        details += f"Parents: {', '.join(parents)}\n"
        
    # Get siblings
    siblings = []
    for pid in person.get('siblings', []):
        s = get_person_by_id(tree_data, pid)
        if s: siblings.append(s.get('name'))
    if siblings:
        details += f"Siblings: {', '.join(siblings)}\n"
        
    # Get children
    children = []
    for pid in person.get('children', []):
        c = get_person_by_id(tree_data, pid)
        if c: children.append(c.get('name'))
    if children:
        details += f"Children: {', '.join(children)}\n"
        
    if 'note' in person:
        details += f"\nAdditional Notes/Research:\n{person['note']}\n"
        
    return details

def generate_biography(query):
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please run: export GEMINI_API_KEY='your-api-key'")
        return
        
    print("Loading family tree data...")
    tree = load_tree('sanderson_tree.json')
    
    person = get_person_by_name_or_id(tree, query)
    if not person:
        print(f"Could not find '{query}' in the family tree.")
        return
        
    print(f"Gathering data for {person.get('name')}...")
    context = format_person_details(person, tree)
    
    prompt = f"""
    You are an expert genealogist and biographer. I have provided you with raw data points 
    from a family tree for an individual.
    
    Please write a beautiful, engaging, and cohesive biography for this person based ONLY on the 
    information provided below. Make it read like a historical narrative rather than a list of facts. 
    If some information is missing, focus on what is provided and frame it elegantly.
    
    RAW DATA:
    {context}
    """
    
    print("\nCalling Gemini 3 API (gemini-3-flash-preview)...\n")
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    
    print("="*60)
    print(f"BIOGRAPHY FOR {person.get('name').upper()}")
    print("="*60)
    print(response.text)
    print("="*60)
    
    # Save to file
    filename = f"{person.get('name', 'Unknown').replace(' ', '_').lower()}_biography.md"
    with open(filename, 'w') as f:
        f.write(f"# Biography: {person.get('name')}\n\n{response.text}")
    print(f"\nSaved biography to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AI Biography from Family Tree")
    parser.add_argument("name", help="The name or ID (e.g. '@I1@') of the person")
    args = parser.parse_args()
    
    generate_biography(args.name)
