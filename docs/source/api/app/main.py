from fastapi import FastAPI, HTTPException
import openai
from scipy.spatial.distance import cosine
import numpy as np
import json

app = FastAPI()
# Load environment variables
load_dotenv()

# Set OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load embeddings from file
with open("../api/data/embeddings.json", "r") as f:
    docs = json.load(f)

# Example: Access embeddings in the chatbot logic
def find_best_match(query_embedding, docs):
    best_doc = None
    min_distance = float("inf")
    for doc in docs:
        distance = np.linalg.norm(np.array(query_embedding) - np.array(doc["embedding"]))
        if distance < min_distance:
            min_distance = distance
            best_doc = doc
    return best_doc

@app.post("/chat")
async def chat(query: str):
    # Embed the query
    query_response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = query_response["data"][0]["embedding"]
    
    # Find the best matching doc
    best_doc = find_best_match(query_embedding, docs)

    # Query OpenAI with relevant content
    openai_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Use the following documentation to answer the question."},
            {"role": "user", "content": f"{best_doc['content']} \n\n User Query: {query}"}
        ]
    )

    return {"response": openai_response['choices'][0]['message']['content']}
