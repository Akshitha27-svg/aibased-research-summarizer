import json
from neo4j import GraphDatabase
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Neo4j connection
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j1234"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# Load abstracts
with open("abstracts_text.json", "r", encoding="utf-8") as f:
    abstracts = json.load(f)   # list ✔

# Convert Abstract ID → Paper ID
def map_to_paper_id(pid):
    if pid.startswith("Abstract"):
        num = pid.split()[-1]
        return f"P{int(num):02d}"
    return pid

paper_ids = []
texts = []

for a in abstracts:
    paper_ids.append(map_to_paper_id(a["paper_id"]))

    # ✅ SAFE TEXT EXTRACTION
    if "abstract" in a:
        texts.append(a["abstract"])
    elif "abstract_text" in a:
        texts.append(a["abstract_text"])
    else:
        texts.append("")   # prevents crash

# TF-IDF similarity
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(texts)
similarity_matrix = cosine_similarity(tfidf_matrix)

STRONG = 0.30
WEAK = 0.10

def create_similarity(tx, p1, p2, score):
    if score >= STRONG:
        tx.run("""
            MATCH (a:Paper {paper_id: $p1})
            MATCH (b:Paper {paper_id: $p2})
            MERGE (a)-[:STRONGLY_RELATED {score: $score}]->(b)
        """, p1=p1, p2=p2, score=score)
    elif score >= WEAK:
        tx.run("""
            MATCH (a:Paper {paper_id: $p1})
            MATCH (b:Paper {paper_id: $p2})
            MERGE (a)-[:SIMILAR_TO {score: $score}]->(b)
        """, p1=p1, p2=p2, score=score)

with driver.session() as session:
    for i in range(len(paper_ids)):
        for j in range(i + 1, len(paper_ids)):
            score = float(similarity_matrix[i][j])
            session.execute_write(
                create_similarity,
                paper_ids[i],
                paper_ids[j],
                score
            )

driver.close()
print("🔥 Abstract similarity relationships added successfully")
