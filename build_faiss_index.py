import numpy as np
import faiss
import pickle

# Load embeddings
embeddings = np.load("embeddings.npy")

print("Embedding shape:", embeddings.shape)

# Get dimension
dimension = embeddings.shape[1]

# Create FAISS index (L2 distance)
index = faiss.IndexFlatL2(dimension)

# Add vectors to index
index.add(embeddings)

print("Total vectors in index:", index.ntotal)

# Save FAISS index
faiss.write_index(index, "faiss_index.index")

print("\nFAISS index saved successfully!")
