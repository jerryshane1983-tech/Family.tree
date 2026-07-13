const fs = require('fs');
const data = JSON.parse(fs.readFileSync('family-tree-app/public/sanderson_tree.json', 'utf8'));

const personMap = new Map();
const cMap = new Map();

data.people.forEach(p => personMap.set(p.id, p));
data.people.forEach(p => {
  if (p.children) {
    if (!cMap.has(p.id)) cMap.set(p.id, new Set());
    p.children.forEach(c => cMap.get(p.id).add(c));
  }
  if (p.parents) {
    p.parents.forEach(parentId => {
      if (!cMap.has(parentId)) cMap.set(parentId, new Set());
      cMap.get(parentId).add(p.id);
    });
  }
});

const buildTree = (rootId, visited = new Set()) => {
  const person = personMap.get(rootId);
  if (!person) return null;
  
  const node = { id: person.id, name: person.name, children: [] };
  
  if (visited.has(rootId)) {
    return node;
  }
  const newVisited = new Set(visited).add(rootId);
  
  const childIds = cMap.get(rootId);
  if (childIds && childIds.size > 0) {
    node.children = Array.from(childIds)
      .map(childId => buildTree(childId, newVisited))
      .filter(child => child !== null);
  }
  return node;
};

const tree = buildTree("@I423@");
console.log(JSON.stringify(tree, null, 2));
