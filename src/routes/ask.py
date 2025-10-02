from fastapi import APIRouter, Body
from src.utils.agentic_runner import AgenticRunner
from src.utils.retriever import WeaviateRetriever
from src.utils.generator import OpenAIGenerator

router = APIRouter()

retriever = WeaviateRetriever()
generator = OpenAIGenerator()
agent = AgenticRunner(retriever, generator)

@router.post("/ask")
def ask(payload: dict = Body(...)):
    question = payload.get("question")
    if not question:
        return {"error": "Missing 'question'"}
    return agent.run(question)
