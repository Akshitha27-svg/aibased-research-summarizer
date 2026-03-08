import pandas as pd
import json
import re

metadata = pd.read_excel("Metadata.xlsx")

# Normalize column names
metadata.columns = metadata.columns.str.strip().str.lower()

# ---- COLUMN DETECTION (ROBUST) ----
paper_col = [c for c in metadata.columns if "paper" in c or c == "id"][0]
author_col = [c for c in metadata.columns if "author" in c][0]
year_col = [c for c in metadata.columns if "year" in c][0]
keyword_col = [c for c in metadata.columns if "keyword" in c][0]

# Journal column: must NOT contain 'year'
journal_candidates = [
    c for c in metadata.columns
    if ("journal" in c or "conference" in c or "venue" in c)
    and "year" not in c
]

journal_col = journal_candidates[0] if journal_candidates else None

# ---- ENTITY STORAGE ----
entities = {
    "papers": [],
    "authors": set(),
    "journals": set(),
    "years": set(),
    "keywords": set()
}

# ---- EXTRACTION ----
for _, row in metadata.iterrows():
    pid = str(row[paper_col]).strip()
    entities["papers"].append(pid)

    # Authors
    if pd.notna(row[author_col]):
        for a in str(row[author_col]).replace(";", ",").split(","):
            entities["authors"].add(a.strip())

    # Journal (ONLY if real journal column exists)
    if journal_col and pd.notna(row[journal_col]):
        journal = str(row[journal_col]).strip()

        # Extra safety: reject pure years
        if not re.fullmatch(r"\d{4}", journal):
            entities["journals"].add(journal)

    # Year
    if pd.notna(row[year_col]):
        entities["years"].add(str(int(row[year_col])))

    # Keywords
    if pd.notna(row[keyword_col]):
        for k in str(row[keyword_col]).split(","):
            k = k.strip()
            if k:
                entities["keywords"].add(k)

# Convert sets → lists
for k in entities:
    if isinstance(entities[k], set):
        entities[k] = sorted(list(entities[k]))

# Save output
with open("entities_output.json", "w", encoding="utf-8") as f:
    json.dump(entities, f, indent=4)

print("✅ entities_output.json regenerated with correct journal normalization")
