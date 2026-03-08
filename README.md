Research Summarizer – Knowledge Graph (Milestone 2)
Project Overview
This project builds a Research Knowledge Graph using Neo4j to model academic papers, authors, journals, keywords, domains, and citation relationships.

The goal is to create a dense and structured research network that allows:
- Paper-to-paper citation analysis
- Author collaboration analysis
- Domain clustering
- Journal mapping
- Reference tracking
Graph Model
•	Nodes:
•	Paper
•	Author
•	Journal
•	Keyword
•	Domain
•	Reference
•	
Relationships:
•	(:Author)-[:WROTE]->(:Paper)
•	(:Paper)-[:PUBLISHED_IN]->(:Journal)
•	(:Paper)-[:HAS_KEYWORD]->(:Keyword)
•	(:Paper)-[:BELONGS_TO]->(:Domain)
•	(:Paper)-[:CITES]->(:Reference)
Project Structure
Research-Summarizer/
│
├── metadata.csv
├── citations.csv
├── research_instances.csv
├── papers_clean.csv
├── papers_extracted.csv
├── extract_papers.py
├── queries.cypher
├── .gitignore
└── README.md
Dataset Description
1) metadata.csv includes:
- Paper ID
- Paper Title
- Primary Author
- Author Affiliations
- Publication Year
- Journal Name
- DOI / Identifier
- Keywords
- Domain

2) research_instances.csv includes:
- Paper_ID
- Ref_ID
- Cited Year
- Reference Title
- Reference Link

Each paper contains approximately 10 references, creating a dense citation network.
How to Import into Neo4j
Step 1: Place CSV files inside the Neo4j import folder.

Step 2: Load Metadata using Cypher queries.

Step 3: Load References using Cypher queries.

Step 4: Visualize Full Knowledge Graph using:
MATCH (n)-[r]-(m)
RETURN n,r,m
LIMIT 1000;
Key Features
•	
•	Multi-layer research knowledge graph
•	Dense citation network
•	Author-paper modeling
•	Domain classification
•	Expandable architecture
•	Scalable for advanced graph analytics
Milestone 2 Completion
- Metadata ingestion completed
- Citation ingestion completed
- Relationships successfully created
- Dense research network built
- Graph fully visualizable
Future Scope
- Co-author network analysis
- Centrality metrics
- Community detection
- Recommendation engine
- Graph Data Science integration
Author
Akshitha Chintakunta
Research Knowledge Graph Project
