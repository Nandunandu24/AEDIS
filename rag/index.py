from sentence_transformers import SentenceTransformer
import faiss
import os

def build_policy_index():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    POLICY_PATH = os.path.join(BASE_DIR, "..", "data_samples", "policies.txt")

    with open(POLICY_PATH, "r") as f:
        policies = f.readlines()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(policies)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "policy_index.faiss")

    with open("policy_texts.txt", "w") as f:
        for p in policies:
            f.write(p.strip() + "\n")

    print("✅ Policy index created successfully")

if __name__ == "__main__":
    build_policy_index()
