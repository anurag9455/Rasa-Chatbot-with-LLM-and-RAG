import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class ProductVectorStore:
    def __init__(self, catalog_path='catalog.csv'):
        self.catalog_path = catalog_path
        self.df = pd.read_csv(catalog_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.embeddings = None
        self._build_index()

    def _build_index(self):
        texts = self.df.apply(lambda row: f"{row['product_name']} by {row['brand']}. Features: {row['features']}", axis=1).tolist()
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)

    def search(self, query, top_k=1):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        results = self.df.iloc[indices[0]].to_dict(orient="records")
        return results
