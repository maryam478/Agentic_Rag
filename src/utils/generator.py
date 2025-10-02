import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """You are a helpful AI assistant.
Ground all answers only in retrieved text.
Always include citations in this format:
[source: <title>]"""

class OpenAIGenerator:
    def generate(self, question: str, hits: list):
        if not hits:
            return {"answer": "I don't know — knowledge base doesn’t cover that.", "grounding": []}

        context = "\n\n".join([f"{h['title']}: {h['text']}" for h in hits])
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Q: {question}\nContext:\n{context}"}
            ],
            max_tokens=300,
        )
        return {
            "answer": resp.choices[0].message.content,
            "grounding": hits
        }
