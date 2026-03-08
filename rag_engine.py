import faiss
import numpy as np
import pandas as pd

metadata = pd.read_csv("Metadata.csv")
index = faiss.read_index("faiss_index.index")

def retrieve_chunks(query_embedding, top_k=5):

    distances, indices = index.search(query_embedding, top_k)

    chunks = []
    papers = []

    for i in indices[0]:
        chunk = metadata.iloc[i]["chunk"]
        paper = metadata.iloc[i]["paper_name"]

        chunks.append(chunk)
        papers.append(paper)

    return chunks, papers