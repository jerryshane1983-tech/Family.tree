import json

with open("sanderson_tree.json", "r") as f:
    data = json.load(f)

# Update Carl Healdton Powell's details
updated = False
for p in data["people"]:
    if p["id"] == "@I204@":
        p["spouse"] = "Shelby Jean Persilver"
        p["children"] = ["@I821@", "@I822@", "@I823@", "@I824@"]
        p["note"] = "Often referred to as Helton Powell. Worked in the oilfields. Predeceased wife in 1992."
        updated = True
        break

if not updated:
    print("Warning: Carl Healdton Powell (@I204@) not found!")

# Add new people
new_people = [
    {
      "id": "@I820@",
      "name": "Shelby Jean Persilver",
      "gender": "F",
      "birth_year": 1938,
      "death_year": 2015,
      "spouse": "Carl Healdton Powell",
      "children": ["@I821@", "@I822@", "@I823@", "@I824@"],
      "note": "Married on April 12, 1956. Buried at Simon Cemetery, Love Co, OK."
    },
    {
      "id": "@I821@",
      "name": "Carl Lee 'Tiny' Powell",
      "gender": "M",
      "birth_year": 1959,
      "death_year": 2020,
      "parents": ["@I204@", "@I820@"],
      "spouse": "Carol Garrett",
      "children": ["@I829@", "@I830@"],
      "note": "CB Handle: 'Tiny'. Truck driver. Resided in Madill, OK. Buried at Powell Cemetery."
    },
    {
      "id": "@I822@",
      "name": "Pat Wayne Powell",
      "gender": "M",
      "birth_year": 1960,
      "death_year": 2021,
      "parents": ["@I204@", "@I820@"],
      "spouse": "Michelle Tupin",
      "children": ["@I825@", "@I826@", "@I827@", "@I828@"],
      "note": "Married January 3, 1992. Oilfield/roustabout worker. Resided in Wilson, OK. Buried at Bomar Point Cemetery."
    },
    {
      "id": "@I823@",
      "name": "Lena Powell",
      "gender": "F",
      "parents": ["@I204@", "@I820@"],
      "spouse": "John Edwards",
      "children": ["@I831@"],
      "note": "Resided in Wilson/Healdton, OK."
    },
    {
      "id": "@I824@",
      "name": "Mike Helton Powell",
      "gender": "M",
      "parents": ["@I204@", "@I820@"],
      "spouse": "Tina Powell",
      "note": "Resided in Healdton, OK."
    },
    {
      "id": "@I840@",
      "name": "Carol Garrett",
      "gender": "F",
      "spouse": "Carl Lee 'Tiny' Powell",
      "children": ["@I829@", "@I830@"]
    },
    {
      "id": "@I841@",
      "name": "Michelle Tupin",
      "gender": "F",
      "spouse": "Pat Wayne Powell",
      "children": ["@I825@", "@I826@", "@I827@", "@I828@"]
    },
    {
      "id": "@I842@",
      "name": "John Edwards",
      "gender": "M",
      "spouse": "Lena Powell",
      "children": ["@I831@"]
    },
    {
      "id": "@I843@",
      "name": "Tina Powell",
      "gender": "F",
      "spouse": "Mike Helton Powell",
      "note": "Predeceased Shelby Jean Powell (before 2015)."
    },
    {
      "id": "@I825@",
      "name": "Roger Powell",
      "gender": "M",
      "parents": ["@I822@", "@I841@"],
      "spouse": "Britney",
      "children": ["@I837@", "@I838@", "@I839@"],
      "note": "2nd Cousin."
    },
    {
      "id": "@I826@",
      "name": "Dillon Powell",
      "gender": "M",
      "parents": ["@I822@", "@I841@"],
      "note": "2nd Cousin."
    },
    {
      "id": "@I827@",
      "name": "Patrick Powell",
      "gender": "M",
      "parents": ["@I822@", "@I841@"],
      "spouse": "Kara Hurst",
      "note": "2nd Cousin."
    },
    {
      "id": "@I828@",
      "name": "Infant Daughter Powell",
      "gender": "F",
      "parents": ["@I822@", "@I841@"],
      "note": "Died in infancy."
    },
    {
      "id": "@I829@",
      "name": "Craig Garrett",
      "gender": "M",
      "parents": ["@I821@", "@I840@"],
      "spouse": "Mhyka",
      "children": ["@I832@", "@I833@", "@I834@", "@I835@", "@I836@"],
      "note": "2nd Cousin. Resides in Madill, OK."
    },
    {
      "id": "@I830@",
      "name": "Cory Garrett",
      "gender": "M",
      "parents": ["@I821@", "@I840@"],
      "spouse": "Sam",
      "note": "2nd Cousin. Resides in Madill, OK."
    },
    {
      "id": "@I831@",
      "name": "Daniel Edwards",
      "gender": "M",
      "parents": ["@I823@", "@I842@"],
      "note": "2nd Cousin."
    },
    {
      "id": "@I832@",
      "name": "Skylar Garrett",
      "gender": "F",
      "parents": ["@I829@", "Mhyka"],
      "note": "Great-grandchild of Carl Helton Powell."
    },
    {
      "id": "@I833@",
      "name": "Jaxxon Garrett",
      "gender": "M",
      "parents": ["@I829@", "Mhyka"],
      "note": "Great-grandchild of Carl Helton Powell."
    },
    {
      "id": "@I834@",
      "name": "Rhyder Garrett",
      "gender": "M",
      "parents": ["@I829@", "Mhyka"],
      "note": "Great-grandchild of Carl Helton Powell."
    },
    {
      "id": "@I835@",
      "name": "Emorie Garrett",
      "gender": "F",
      "parents": ["@I829@", "Mhyka"],
      "note": "Great-grandchild of Carl Helton Powell."
    },
    {
      "id": "@I836@",
      "name": "Carson Garrett",
      "gender": "M",
      "parents": ["@I829@", "Mhyka"],
      "note": "Great-grandchild of Carl Helton Powell."
    },
    {
      "id": "@I837@",
      "name": "Hayden Powell",
      "gender": "M",
      "parents": ["@I825@", "Britney"],
      "note": "Great-grandchild of Carl Helton Powell."
    },
    {
      "id": "@I838@",
      "name": "Allysin Powell",
      "gender": "F",
      "parents": ["@I825@", "Britney"],
      "note": "Great-grandchild of Carl Helton Powell."
    },
    {
      "id": "@I839@",
      "name": "Kynnedi Powell",
      "gender": "F",
      "parents": ["@I825@", "Britney"],
      "note": "Great-grandchild of Carl Helton Powell."
    }
]

data["people"].extend(new_people)

with open("sanderson_tree.json", "w") as f:
    json.dump(data, f, indent=2)

print("Successfully updated sanderson_tree.json with Carl Helton Powell's branch.")
