import os
import json
import openai
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = "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"

# Path to Sphinx-generated HTML files
HTML_DIRECTORY = "../_build/html/"  # Or adjust the path if necessary

# Path to store the embeddings
EMBEDDING_FILE = "../api/data/embeddings.json"  # Or /scripts/data/embeddings.json

# Extract content from Sphinx HTML
def extract_text_from_html(directory):
    docs = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)
                    if text:
                        docs.append({"title": filename, "content": text})
    return docs

# Generate embeddings using OpenAI
def create_embeddings(docs):
    for doc in docs:
        response = openai.Embedding.create(
            input=doc["content"],
            model="text-embedding-ada-002"  # Or any other embedding model
        )
        doc["embedding"] = response["data"][0]["embedding"]
    return docs

# Save embeddings to JSON
def save_embeddings(docs, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=4)

# Main script
if __name__ == "__main__":
    # Step 1: Extract content from Sphinx HTML
    html_docs = extract_text_from_html(HTML_DIRECTORY)

    # Step 2: Create embeddings
    embedded_docs = create_embeddings(html_docs)

    # Step 3: Save embeddings to a file
    save_embeddings(embedded_docs, EMBEDDING_FILE)

    print(f"✅ Embeddings saved to {EMBEDDING_FILE}")
