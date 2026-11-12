import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_embedding(text):
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(A,B):
    dot_product = np.dot(A,B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    return dot_product / (norm_A * norm_B)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_FOLDER = os.getenv("KB_FOLDER") or "knowledge_base"

def load_documents(folder = KB_FOLDER):
    documents=[]
    folder_path = Path(folder)
    if not folder_path.is_absolute():
        folder_path = PROJECT_ROOT / folder_path

    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        path = folder_path / filename
        with open(path,"r",encoding="utf-8") as f:
            text = f.read()
            documents.append({
                "source": filename,
                "text": text,
            })

    return documents


def add_embeddings(documents):

    for doc in documents:
        vector = get_embedding(doc["text"])
        doc["vector"] = vector

    return documents


def search(query,documents,top_k=3):
    query_vector = get_embedding(query)
    results=[]
    for doc in documents:
        score = cosine_similarity(query_vector, doc["vector"])
        results.append({
            "score":score,
            "source":doc["source"],
            "text":doc["text"],
            "size":len(doc["text"])

        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]


def testing(user_query,documents,top_k=3):
    print(f"\nUser query: {user_query}")

    results = search(user_query,documents,top_k)

    print(f"\nTop {top_k} results:")
    for r in results:
        print(f"Score: {r['score']:.2f}, Source: {r['source']}, Size: {r['size']} characters")


documents = load_documents()
documents = add_embeddings(documents)
print(f"we have embedded {len(documents)} documents.")

user_query = "how many days i will get maternity leave?"
testing(user_query,documents,top_k=3)