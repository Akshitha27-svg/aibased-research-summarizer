import json
from neo4j import GraphDatabase

# ---- Neo4j connection ----
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j1234"   # ← EXACT password you set

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# ---- Load citations JSON ----
with open("citations.json", "r", encoding="utf-8") as f:
    citations = json.load(f)

def create_cites(tx, citing, cited):
    tx.run("""
        MATCH (p1:Paper {paper_id: $citing})
        MATCH (p2:Paper {paper_id: $cited})
        MERGE (p1)-[:CITES]->(p2)
    """, citing=citing, cited=cited)

with driver.session() as session:
    for row in citations:
        citing = row.get("Paper_ID")
        cited = row.get("Cross Link Paper ID")

        # ✅ Skip invalid citations
        if not citing or not cited or cited == 0:
            continue

        session.execute_write(create_cites, citing, cited)

driver.close()
print("✅ Citations loaded successfully into Neo4j")
