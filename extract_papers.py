import fitz  # PyMuPDF
import os
import pandas as pd

pdf_folder = "C:\\Users\\lenovo\\OneDrive\\Desktop\\Research Summarizer\\Research papers"

papers = []

for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        path = os.path.join(pdf_folder, filename)
        doc = fitz.open(path)

        text = ""
        for page in doc:
            text += page.get_text()

        title = text.split("\n")[0]
        abstract_start = text.lower().find("abstract")

        if abstract_start != -1:
            abstract = text[abstract_start:abstract_start+1000]
        else:
            abstract = text[:1000]

        papers.append({
            "paper_id": filename.replace(".pdf",""),
            "title": title.strip(),
            "abstract": abstract.strip()
        })

df = pd.DataFrame(papers)
df.to_csv("papers_extracted.csv", index=False)

print("Extraction complete.")
