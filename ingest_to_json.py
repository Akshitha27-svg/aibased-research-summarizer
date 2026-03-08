import os
import json
import pandas as pd
import pdfplumber

# ==================================================
# BASE PATHS
# ==================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ABSTRACTS_DIR = os.path.join(BASE_DIR, "Abstracts")
PAPERS_DIR = os.path.join(BASE_DIR, "Research papers")

METADATA_FILE = os.path.join(BASE_DIR, "Metadata.xlsx")
CITATIONS_FILE = os.path.join(BASE_DIR, "Citations.xlsx")
REFERENCES_FILE = os.path.join(BASE_DIR, "Research_References.xlsx")

OUTPUT_DIR = os.path.join(BASE_DIR, "output_json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# PDF TEXT EXTRACTION
# ==================================================
def extract_pdf_text(pdf_path):
    text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")
    return "\n".join(text)

# ==================================================
# LOAD EXCEL FILES
# ==================================================
metadata_df = pd.read_excel(METADATA_FILE)
citations_df = pd.read_excel(CITATIONS_FILE)
references_df = pd.read_excel(REFERENCES_FILE)

# Normalize column names
metadata_df.columns = metadata_df.columns.astype(str)
citations_df.columns = citations_df.columns.astype(str)
references_df.columns = references_df.columns.astype(str)

# ==================================================
# AUTO-DETECT PAPER ID COLUMN
# ==================================================
def find_paper_id_column(df):
    for col in df.columns:
        normalized = col.replace(" ", "").replace("_", "").lower()
        if normalized in ["paperid", "id", "documentid"]:
            return col
    return None

META_ID_COL = find_paper_id_column(metadata_df)
CIT_ID_COL = find_paper_id_column(citations_df)
REF_ID_COL = find_paper_id_column(references_df)

if META_ID_COL is None:
    raise ValueError("❌ No Paper ID column found in Metadata.xlsx")

# ==================================================
# INGEST + NORMALIZE TO JSON
# ==================================================
for _, row in metadata_df.iterrows():
    paper_id = str(row[META_ID_COL]).strip()

    abstract_pdf = os.path.join(ABSTRACTS_DIR, f"{paper_id}.pdf")
    paper_pdf = os.path.join(PAPERS_DIR, f"{paper_id}.pdf")

    abstract_text = extract_pdf_text(abstract_pdf) if os.path.exists(abstract_pdf) else ""
    full_text = extract_pdf_text(paper_pdf) if os.path.exists(paper_pdf) else ""

    citations = []
    if CIT_ID_COL:
        citations = citations_df[citations_df[CIT_ID_COL].astype(str) == paper_id].to_dict(orient="records")

    references = []
    if REF_ID_COL:
        references = references_df[references_df[REF_ID_COL].astype(str) == paper_id].to_dict(orient="records")

    paper_json = {
        "paper_id": paper_id,
        "title": row.get("Title", row.get("title", "")),
        "abstract": abstract_text,
        "full_text": full_text,
        "metadata": row.to_dict(),
        "citations": citations,
        "references": references
    }

    output_path = os.path.join(OUTPUT_DIR, f"{paper_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(paper_json, f, indent=4, ensure_ascii=False)

    print(f"✅ Created {paper_id}.json")

print("\n🎯 INGESTION COMPLETE")
print(f"📂 JSON files saved to: {OUTPUT_DIR}")
