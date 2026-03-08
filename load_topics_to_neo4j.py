import json
from neo4j import GraphDatabase
import re

# -------------------------------
# Neo4j connection
# -------------------------------
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j1234"   # ← use your real password

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# -------------------------------
# Helper: Convert "Abstract 1" → "P01"
# -------------------------------
def abstract_to_paper_id(abstract_id):
    number = re.findall(r"\d+", abstract_id)[0]  # extract number
    return f"P{int(number):02d}"                  # zero padded

# -------------------------------
# Load topics JSON
# -------------------------------
with open("topics.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def create_topics(tx, paper_id, topics):
    for topic in topics:
        tx.run("""
            MATCH (p:Paper {paper_id: $paper_id})
            MERGE (t:Topic {name: $topic})
            MERGE (p)-[:HAS_TOPIC]->(t)
        """, paper_id=paper_id, topic=topic)

# -------------------------------
# Write to Neo4j
# -------------------------------
with driver.session() as session:
    for entry in data:
        fixed_paper_id = abstract_to_paper_id(entry["paper_id"])
        session.execute_write(
            create_topics,
            fixed_paper_id,
            entry["topics"]
        )

driver.close()

print("✅ Topics successfully linked to Papers")
