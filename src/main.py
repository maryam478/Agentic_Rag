import argparse
import uvicorn
from fastapi import FastAPI, Body
from src.utils.retriever import WeaviateRetriever
from src.utils.generator import OpenAIGenerator
from src.utils.agentic_runner import AgenticRunner

retriever = WeaviateRetriever()
generator = OpenAIGenerator()
agent = AgenticRunner(retriever, generator)

app = FastAPI(title="RAG Agent with LangGraph")

@app.post("/ask")
def ask_endpoint(payload: dict = Body(...)):
    question = payload.get("question")
    if not question:
        return {"error": "Missing question"}
    return agent.run(question)

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=str, help="Question")
    args = parser.parse_args()
    if args.q:
        print(agent.run(args.q))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cli()
    else:
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)
