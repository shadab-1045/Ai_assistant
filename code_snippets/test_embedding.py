from openai import OpenAI
import os
from dotenv import load_dotenv

# Read local API credentials and model settings before creating the client.
load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# A batch request returns one embedding vector for each input string.
response = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input=["Hello, my dog is cute", "What is the capital of France?"]
)
print(len(response.data[0].embedding))
print(len(response.data[1].embedding))