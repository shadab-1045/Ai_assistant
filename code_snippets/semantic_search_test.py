from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np

# Load the API endpoint, credentials, and embedding model from the local .env file.
load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_embedding(text):
    """Convert one text string into a vector using the configured embedding model."""
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(A,B):
    """Measure the cosine similarity between two embedding vectors."""
    dot_product = np.dot(A,B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    return dot_product / (norm_A * norm_B)


# Similar topics should generally have higher cosine similarity than unrelated ones.
text1 = "python is a programming language"
text2= "python is used to write scripts and applications"
text3 = "the capital of France is Paris"

A = get_embedding(text1)
B = get_embedding(text2)
C = get_embedding(text3)

similarity_AB = cosine_similarity(A, B)
similarity_AC = cosine_similarity(A, C)
similarity_BC = cosine_similarity(B, C)

print(f"Similarity between text1 and text2: {similarity_AB:.4f}")
print(f"Similarity between text1 and text3: {similarity_AC:.4f}")
print(f"Similarity between text2 and text3: {similarity_BC:.4f}")