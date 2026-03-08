import os
import json
import PyPDF2

# Folder containing PDF abstracts (EXACT name from your system)
PDF_DIR = "Abstracts"

# Output JSON file
OUTPUT_FILE = "abstracts_text.json"

# Safety check
if not os.path.exists(PDF_DIR):
    raise FileNotFoundError(f"❌ Folder not found: {PDF_DIR}")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.strip()

abstracts = []

for file in os.listdir(PDF_DIR):
    if file.lower().endswith(".pdf"):
        paper_id = os.path.splitext(file)[0]   # P01, P02, etc
        pdf_path = os.path.join(PDF_DIR, file)

        print(f"📄 Reading {file}")

        abstract_text = extract_text_from_pdf(pdf_path)

        if abstract_text:
            abstracts.append({
                "paper_id": paper_id,
                "abstract": abstract_text
            })

# Save extracted abstracts
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(abstracts, f, indent=4, ensure_ascii=False)

print("\n✅ Abstract extraction completed")
print(f"📁 Output file: {OUTPUT_FILE}")
print(f"📊 Total abstracts extracted: {len(abstracts)}")
