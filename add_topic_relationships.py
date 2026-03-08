import json
from neo4j import GraphDatabase

# -------------------------------
# Neo4j connection
# -------------------------------
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j1234"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# -------------------------------
# Load topics JSON (LIST format)
# -------------------------------
with open("topics.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def create_topic_rel(tx, paper_id, topic):
    tx.run("""
        MATCH (p:Paper {paper_id: $paper_id})
        MERGE (t:Topic {name: $topic})
        MERGE (p)-[:HAS_TOPIC]->(t)
    """, paper_id=paper_id, topic=topic)

with driver.session() as session:
    for item in data:
        raw_id = item["paper_id"]   # "Abstract 1"
        topics = item["topics"]

        # 🔑 Convert "Abstract 1" → "P01"
        number = raw_id.split()[-1]
        paper_id = f"P{int(number):02d}"

        for topic in topics:
            session.execute_write(
                create_topic_rel,
                paper_id,
                topic
            )

driver.close()

print("✅ Topic relationships created successfully")
