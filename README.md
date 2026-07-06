# 🌳 Sanderson & Powell Family Tree Project

Welcome to your family tree backup and research repository. 

When you view this repository on GitHub, the diagram below will automatically render into an interactive graphical chart showing your ancestral branches and descendants!

---

## 📍 Family Tree Diagram

```mermaid
graph TD
    classDef target fill:#ffb3ba,stroke:#ff6b6b,stroke-width:2px;
    classDef relative fill:#bae1ff,stroke:#5c8ae6,stroke-width:1px;

    %% Ancestors
    Otto["L. Otto Oliver Powell<br/>(1872 - 1938)"]:::relative --- Aulmeady["Aulmeady Mae Dennis<br/>(1892 - 1968)"]:::relative
    
    Otto --> BoBo["Garland Thomas 'Bo Bo' Powell<br/>(1928 - 2001)"]:::relative
    Otto --> CarlH["Carl Healdton Powell<br/>(d. 1992)"]:::relative
    
    %% Bo Bo's Branch
    BoBo --- PearlM["Pearl Edith Marshall<br/>(1928 - 1991)"]:::relative
    PearlM --> Mossie["Pearl Anne 'Mossie' Powell"]:::relative
    PearlM --> CarlR["Carl Robert Powell"]:::relative
    PearlM --> Tommy["Thomas 'Tommy' Powell"]:::relative
    
    %% Carl Helton's Branch (Grandpa's Brother)
    CarlH --- Shelby["Shelby Jean Persilver<br/>(1938 - 2015)"]:::relative
    Shelby --> Lee["Carl Lee 'Tiny' Powell<br/>(1959 - 2020)"]:::relative
    Shelby --> Pat["Pat Wayne Powell<br/>(1960 - 2021)"]:::relative
    Shelby --> Lena["Lena Powell (Edwards)"]:::relative
    Shelby --> Mike["Mike Helton Powell"]:::relative
    
    %% Your Branch
    Mossie --- Freddie["Freddie Ray Sanderson Jr."]:::relative
    Freddie --> Jerry["Jerry Shane Sanderson<br/>(You)"]:::target
```

---

## 🗂️ Project Directory Files

*   **Database:** [sanderson_tree.json](sanderson_tree.json) — Complete JSON database containing all 221 individuals and relationships.
*   **Visual Web App:** [family-tree-app/](family-tree-app/) — A React + Vite interactive family tree application.
*   **Research Reports:**
    *   [carl_powell_descendants.md](carl_powell_descendants.md) — Comprehensive report on Carl Helton Powell's descendants.
    *   [KRAKEN_MASTER_DOSSIER.md](KRAKEN_MASTER_DOSSIER.md) — Active OSINT intelligence dossier on key targets.
