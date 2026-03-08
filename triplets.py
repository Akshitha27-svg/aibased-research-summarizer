import json
import os

# ==========================================
# CONFIG
# ==========================================

RELATIONSHIPS_FILE = "normalized_json/relationships_output.json"
OUTPUT_FILE = "normalized_json/triplets_output.json"

# ==========================================
# LOAD RELATIONSHIPS
# ==========================================

with open(RELATIONSHIPS_FILE, "r", encoding="utf-8") as f:
    relationships = json.load(f)

# ==========================================
# CONVERT TO TRIPLETS
# ==========================================

triplets = []

for rel in relationships:
    triplets.append({
        "subject": rel["source"],
        "predicate": rel["relation"],
        "object": rel["target"]
    })

# ==========================================
# SAVE OUTPUT
# ==========================================

os.makedirs("normalized_json", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(triplets, f, indent=4, ensure_ascii=False)

print("✔ Triplets created successfully")
print(f"📄 Output file: {OUTPUT_FILE}")
print(f"🔗 Total triplets: {len(triplets)}")
