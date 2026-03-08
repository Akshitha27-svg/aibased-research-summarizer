import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Load chunked data
df = pd.read_csv("chunks.csv")

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(
    df["chunk"].tolist(),
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Embedding shape:", embeddings.shape)

# Save embeddings
np.save("embeddings.npy", embeddings)

# Save metadata separately (paper name + chunk)
df.to_pickle("chunks_metadata.pkl")

print("\nEmbeddings saved successfully!")
