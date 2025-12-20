import os
import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "policy_index.faiss")
TEXT_PATH = os.path.join(BASE_DIR, "policy_texts.txt")

def retrieve_policies(query, top_k=2):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(INDEX_PATH)

    with open(TEXT_PATH, "r") as f:
        policies = f.readlines()

    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, top_k)

    return [policies[i].strip() for i in indices[0]]
