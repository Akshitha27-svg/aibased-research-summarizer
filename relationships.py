import pandas as pd
import json
import os
import re

# =====================================================
# CONFIG
# =====================================================

METADATA_FILE = "Metadata.xlsx"
OUTPUT_DIR = "normalized_json"
OUTPUT_FILE = "relationships_output.json"

# =====================================================
# HELPERS
# =====================================================

def find_column(columns, keywords):
    for col in columns:
        for key in keywords:
            if key in col.lower():
                return col
    return None


def split_values(text):
    if pd.isna(text):
        return []
    return [v.strip() for v in re.split(r";|,|\|", str(text)) if v.strip()]


# =====================================================
# PIPELINE
# =====================================================

def generate_relationships():
    df = pd.read_excel(METADATA_FILE)

    paper_col   = find_column(df.columns, ["paper"])
    author_col  = find_column(df.columns, ["author"])
    journal_col = find_column(df.columns, ["journal"])
    year_col    = find_column(df.columns, ["year"])
    keyword_col = find_column(df.columns, ["keyword"])

    if not paper_col:
        raise ValueError("Paper_ID column not found in Metadata.xlsx")

    relationships = []

    for _, row in df.iterrows():
        paper_id = str(row[paper_col]).strip()

        if author_col:
            for author in split_values(row[author_col]):
                relationships.append({
                    "source": paper_id,
                    "relation": "WRITTEN_BY",
                    "target": author
                })

        if journal_col and not pd.isna(row[journal_col]):
            relationships.append({
                "source": paper_id,
                "relation": "PUBLISHED_IN",
                "target": str(row[journal_col]).strip()
            })

        if year_col and not pd.isna(row[year_col]):
            relationships.append({
                "source": paper_id,
                "relation": "PUBLISHED_YEAR",
                "target": str(int(row[year_col]))
            })

        if keyword_col:
            for kw in split_values(row[keyword_col]):
                relationships.append({
                    "source": paper_id,
                    "relation": "HAS_KEYWORD",
                    "target": kw
                })

    return relationships


# =====================================================
# SAVE OUTPUT
# =====================================================

def save_relationships(data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return path


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    relationships = generate_relationships()
    output_path = save_relationships(relationships)

    print("✔ Relationships generated successfully")
    print(f"📄 Output file: {output_path}")
    print(f"🔗 Total relationships: {len(relationships)}")
