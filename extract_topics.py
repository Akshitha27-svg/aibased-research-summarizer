import json
import re
from collections import Counter

INPUT_FILE = "abstracts_text.json"
OUTPUT_FILE = "topics.json"

def extract_keywords(text):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    stopwords = {
        "this","that","with","from","were","which","their","using",
        "based","paper","study","method","results","proposed"
    }
    words = [w for w in words if w not in stopwords]
    return [w for w, _ in Counter(words).most_common(5)]

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    abstracts = json.load(f)

topics_data = []

for row in abstracts:
    topics_data.append({
        "paper_id": row["paper_id"],
        "topics": extract_keywords(row["abstract"])
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(topics_data, f, indent=4)

print("✅ topics.json created")
