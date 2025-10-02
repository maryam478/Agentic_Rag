import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBED_MODEL = "text-embedding-3-small"

class OpenAIEmbedder:
    def embed_text(self, text: str):
        resp = client.embeddings.create(model=EMBED_MODEL, input=text)
        return resp.data[0].embedding
