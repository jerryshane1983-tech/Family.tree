import React, { useState, useMemo, useEffect, Suspense, lazy, useRef } from 'react';
import gsap from 'gsap';
import './App.css';

const Tree = lazy(() => import('react-d3-tree'));

const buildTree = (rootId, personMap, childrenMap, visited = new Set()) => {
  const person = personMap.get(rootId);
  if (!person) return null;

  // Find spouses/co-parents based on the children's parent arrays
  const spouses = new Map();
  const childIds = childrenMap.get(rootId);
  if (childIds && childIds.size > 0) {
    childIds.forEach(childId => {
      const child = personMap.get(childId);
      if (child && child.parents) {
        child.parents.forEach(parentId => {
          if (parentId !== rootId) {
            spouses.set(parentId, personMap.get(parentId));
          }
        });
      }
    });
  }

  const spouseNames = Array.from(spouses.values()).map(s => s ? s.name : '').filter(Boolean).join(', ');

  let dateString = null;
  const bYear = person.birth_date ? person.birth_date.split('-')[0] : person.birth_year ? String(person.birth_year) : null;
  const dYear = person.death_date ? person.death_date.split('-')[0] : person.death_year ? String(person.death_year) : null;
  if (bYear && dYear) {
    dateString = `${bYear} - ${dYear}`;
  } else if (bYear && !dYear) {
    dateString = `b. ${bYear}`;
  } else if (!bYear && dYear) {
    dateString = `d. ${dYear}`;
  }

  const node = {
    name: person.name,
    attributes: {
      dates: dateString,
      gender: person.gender === 'M' ? 'Male' : person.gender === 'F' ? 'Female' : 'Unknown',
      spouse: spouseNames || null
    },
    children: []
  };

  if (visited.has(rootId)) {
    node.attributes.duplicate = true;
    return node;
  }

  const newVisited = new Set(visited).add(rootId);

  if (childIds && childIds.size > 0) {
    node.children = Array.from(childIds)
      .map(childId => buildTree(childId, personMap, childrenMap, newVisited))
      .filter(child => child !== null);
  }

  if (node.children.length === 0) {
    delete node.children;
  }

  return node;
};

// Custom React Component for the Node to handle its own GSAP animations
const GlassNode = ({ nodeDatum, toggleNode }) => {
  const cardRef = useRef(null);

  useEffect(() => {
    // Antigravity Entrance Animation
    gsap.fromTo(cardRef.current, 
      { opacity: 0, scale: 0.8, y: 30, rotationX: 15 },
      { opacity: 1, scale: 1, y: 0, rotationX: 0, duration: 0.8, ease: "power3.out", delay: 0.05 }
    );
  }, []);

  const handleHover = () => {
    gsap.to(cardRef.current, { scale: 1.05, y: -5, boxShadow: "0 20px 40px rgba(79, 172, 254, 0.2)", duration: 0.3, ease: "power2.out" });
  };

  const handleLeave = () => {
    gsap.to(cardRef.current, { scale: 1, y: 0, boxShadow: "0 10px 30px rgba(0, 0, 0, 0.3)", duration: 0.5, ease: "power2.out" });
  };

  const isMale = nodeDatum.attributes?.gender === 'Male';
  const isFemale = nodeDatum.attributes?.gender === 'Female';

  return (
    <foreignObject x="-125" y="-75" width="250" height="150" style={{ overflow: 'visible' }}>
      <div 
        ref={cardRef}
        className={`glass-card ${isMale ? 'glass-male' : isFemale ? 'glass-female' : 'glass-unknown'}`}
        onMouseEnter={handleHover}
        onMouseLeave={handleLeave}
      >
        <div className="glass-content">
          <h3 className="glass-name">{nodeDatum.name}</h3>
          {(nodeDatum.attributes?.dates || nodeDatum.attributes?.duplicate) && (
            <p className="glass-dates">
              {nodeDatum.attributes?.dates}
              {nodeDatum.attributes?.duplicate && <span className="duplicate-tag"> (Repeated)</span>}
            </p>
          )}
          {nodeDatum.attributes?.spouse && (
            <p className="glass-spouse" style={{ fontSize: '0.8rem', color: '#fbbf24', marginTop: '4px' }}>
              &amp; {nodeDatum.attributes.spouse}
            </p>
          )}
        </div>
        
        {nodeDatum.children && (
          <button className="glass-expand-btn" onClick={toggleNode}>
            {nodeDatum.__rd3t.collapsed ? '▼ Expand' : '▲ Collapse'}
          </button>
        )}
      </div>
    </foreignObject>
  );
};

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRootId, setSelectedRootId] = useState(null);
  const [treeData, setTreeData] = useState(null);

  useEffect(() => {
    fetch('/sanderson_tree.json')
      .then(res => res.json())
      .then(data => {
        setTreeData(data);
      });
  }, []);

  const { personMap, allPeople, childrenMap } = useMemo(() => {
    const map = new Map();
    const cMap = new Map();
    
    if (!treeData) return { personMap: map, allPeople: [], childrenMap: cMap };
    
    treeData.people.forEach(p => map.set(p.id, p));
    
    treeData.people.forEach(p => {
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

    return { personMap: map, allPeople: treeData.people, childrenMap: cMap };
  }, [treeData]);

  const filteredPeople = useMemo(() => {
    if (!searchTerm) return [];
    return allPeople.filter(p => p.name.toLowerCase().includes(searchTerm.toLowerCase()));
  }, [searchTerm, allPeople]);

  const treeDataFormatted = useMemo(() => {
    if (!selectedRootId) return null;
    return buildTree(selectedRootId, personMap, childrenMap);
  }, [selectedRootId, personMap, childrenMap]);

  return (
    <div className="app-container">
      {/* Background elements for Antigravity depth */}
      <div className="ambient-orb orb-1"></div>
      <div className="ambient-orb orb-2"></div>

      <header className="header antigravity-header">
        <h1>Sanderson Family Tree</h1>
        <p>Interactive Spatial Explorer</p>
        {!selectedRootId && (
          <div className="search-bar">
            <input 
              type="text" 
              placeholder="Search for a person to view their descendants..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        )}
      </header>

      {!selectedRootId && (
        <div className="search-results antigravity-results">
          {searchTerm && filteredPeople.length > 0 && (
            <ul className="results-list">
              {filteredPeople.map(p => {
                const bY = p.birth_date ? p.birth_date.split('-')[0] : p.birth_year ? String(p.birth_year) : '?';
                const dY = p.death_date ? p.death_date.split('-')[0] : p.death_year ? String(p.death_year) : '?';
                const showDates = bY !== '?' || dY !== '?';
                return (
                  <li key={p.id} onClick={() => { setSelectedRootId(p.id); setSearchTerm(''); }}>
                    {p.name} {showDates && <span className="dates">({bY} - {dY})</span>}
                  </li>
                );
              })}
            </ul>
          )}
          {searchTerm && filteredPeople.length === 0 && (
            <p className="no-results">No one found matching "{searchTerm}"</p>
          )}
        </div>
      )}

      {selectedRootId && treeDataFormatted && (
        <main className="tree-container">
          <button className="back-btn glass-btn" onClick={() => setSelectedRootId(null)}>← Select different starting person</button>
          <Suspense fallback={<div className="loading-state">Initializing Antigravity Engine...</div>}>
            <Tree 
              data={treeDataFormatted} 
              orientation="vertical" 
              pathFunc="step" 
              nodeSize={{ x: 300, y: 220 }}
              renderCustomNodeElement={(rd3tProps) => <GlassNode {...rd3tProps} />}
              translate={{ x: window.innerWidth / 2, y: 150 }}
              separation={{ siblings: 1.2, nonSiblings: 1.5 }}
              transitionDuration={600}
            />
          </Suspense>
        </main>
      )}
    </div>
  );
}
