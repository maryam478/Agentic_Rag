import os, weaviate
from src.utils.embed import OpenAIEmbedder

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME", "KnowledgeChunk")

client = weaviate.Client(url=WEAVIATE_URL)

class WeaviateRetriever:
    def __init__(self, class_name=CLASS_NAME, threshold: float = 0.35):
        self.class_name = class_name
        self.embedder = OpenAIEmbedder()
        self.threshold = threshold

    def retrieve(self, query: str, top_k: int = 5):
        q_emb = self.embedder.embed_text(query)
        res = (
            client.query.get(self.class_name, ["title", "text"])
            .with_near_vector({"vector": q_emb})
            .with_additional(["distance"])
            .with_limit(top_k)
            .do()
        )
        raw = res.get("data", {}).get("Get", {}).get(self.class_name, [])
        return [
            {
                "title": h["title"],
                "text": h["text"],
                "distance": h["_additional"]["distance"],
            }
            for h in raw if h["_additional"]["distance"] <= self.threshold
        ]
