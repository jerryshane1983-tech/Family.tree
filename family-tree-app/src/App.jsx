import React, { useState, useMemo, useEffect, Suspense, lazy, useRef } from 'react';
import gsap from 'gsap';
import { GoogleGenAI } from '@google/genai';
import './App.css';

const Tree = lazy(() => import('react-d3-tree'));

const buildTree = (rootId, personMap, childrenMap, visited = new Set()) => {
  const person = personMap.get(rootId);
  if (!person) return null;

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
    id: person.id,
    name: person.name,
    attributes: {
      dates: dateString,
      gender: person.gender === 'M' ? 'Male' : person.gender === 'F' ? 'Female' : 'Unknown',
      spouse: spouseNames || null,
      raw: person
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

const GlassNode = ({ nodeDatum, toggleNode, onGenerateBio }) => {
  const cardRef = useRef(null);

  useEffect(() => {
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
    <foreignObject x="-125" y="-90" width="250" height="180" style={{ overflow: 'visible' }}>
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
          <button 
            className="glass-bio-btn" 
            onClick={(e) => { e.stopPropagation(); onGenerateBio(nodeDatum); }}
          >
            ✨ AI Biography
          </button>
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
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '');
  
  // Modal State
  const [bioModal, setBioModal] = useState({ open: false, person: null, text: '', loading: false });

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}sanderson_tree.json?t=${Date.now()}`)
      .then(res => res.json())
      .then(data => {
        setTreeData(data);
      });
  }, []);

  const handleApiKeyChange = (e) => {
    setApiKey(e.target.value);
    localStorage.setItem('gemini_api_key', e.target.value);
  };

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

  // Handle Biography Generation
  const generateBiography = async (nodeDatum) => {
    if (!apiKey) {
      alert("Please enter your Gemini API Key in the top right corner first!");
      return;
    }

    setBioModal({ open: true, person: nodeDatum.name, text: '', loading: true });
    
    const person = nodeDatum.attributes.raw;
    let details = `Name: ${person.name}\n`;
    if (person.birth_date) details += `Birth: ${person.birth_date}\n`;
    if (person.birth_place) details += `Birth Place: ${person.birth_place}\n`;
    
    const parents = (person.parents || []).map(id => personMap.get(id)?.name).filter(Boolean);
    if (parents.length) details += `Parents: ${parents.join(', ')}\n`;
    
    const siblings = (person.siblings || []).map(id => personMap.get(id)?.name).filter(Boolean);
    if (siblings.length) details += `Siblings: ${siblings.join(', ')}\n`;
    
    const children = (person.children || []).map(id => personMap.get(id)?.name).filter(Boolean);
    if (children.length) details += `Children: ${children.join(', ')}\n`;
    
    if (person.note) details += `Notes: ${person.note}\n`;

    const prompt = `You are an expert genealogist. Write a beautiful, engaging historical biography for ${person.name} based ONLY on this raw family tree data. Format it with HTML paragraphs (<p>). Data:\n${details}`;

    try {
      // NOTE: Using fetch to directly hit REST API to avoid browser compatibility issues with the SDK
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }]
        })
      });
      
      const result = await response.json();
      if (result.error) throw new Error(result.error.message);
      
      const text = result.candidates[0].content.parts[0].text;
      setBioModal({ open: true, person: nodeDatum.name, text: text, loading: false });
    } catch (error) {
      console.error(error);
      setBioModal({ open: true, person: nodeDatum.name, text: `<p style="color:red">Error: ${error.message}</p>`, loading: false });
    }
  };

  return (
    <div className="app-container">
      <div className="api-key-input">
        <input 
          type="password" 
          placeholder="Enter Gemini API Key..." 
          value={apiKey} 
          onChange={handleApiKeyChange}
        />
      </div>

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
              nodeSize={{ x: 300, y: 240 }}
              renderCustomNodeElement={(rd3tProps) => <GlassNode {...rd3tProps} onGenerateBio={generateBiography} />}
              translate={{ x: window.innerWidth / 2, y: 150 }}
              separation={{ siblings: 1.2, nonSiblings: 1.5 }}
              transitionDuration={600}
            />
          </Suspense>
        </main>
      )}

      {/* Biography Modal */}
      {bioModal.open && (
        <div className="bio-modal-overlay" onClick={() => setBioModal({ ...bioModal, open: false })}>
          <div className="bio-modal-content" onClick={e => e.stopPropagation()}>
            <button className="bio-close-btn" onClick={() => setBioModal({ ...bioModal, open: false })}>×</button>
            <h2>{bioModal.person}</h2>
            {bioModal.loading ? (
              <div className="loading-state">Gemini 3 is writing the biography...</div>
            ) : (
              <div dangerouslySetInnerHTML={{ __html: bioModal.text }} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
