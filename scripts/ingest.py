import os
import weaviate
from src.utils.chunk import chunk_text
from src.utils.embed import OpenAIEmbedder

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME", "KnowledgeChunk")

client = weaviate.Client(WEAVIATE_URL)
embedder = OpenAIEmbedder()

def create_schema():
    schema = {
        "classes": [
            {
                "class": CLASS_NAME,
                "properties": [
                    {"name": "title", "dataType": ["string"]},
                    {"name": "text", "dataType": ["text"]},
                ]
            }
        ]
    }
    client.schema.delete_all()
    client.schema.create(schema)

def ingest_file(filepath):
    with open(filepath, "r") as f:
        text = f.read()
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    with client.batch(batch_size=20) as batch:
        for i, chunk in enumerate(chunks):
            vec = embedder.embed_text(chunk)
            client.batch.add_data_object(
                {"title": os.path.basename(filepath), "text": chunk},
                CLASS_NAME,
                vector=vec
            )
    print(f"Ingested {len(chunks)} chunks from {filepath}")

if __name__ == "__main__":
    create_schema()
    ingest_file("data/scraped_data.txt")
