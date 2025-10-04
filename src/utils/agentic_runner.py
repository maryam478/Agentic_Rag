# src/utils/agentic_runner.py
from src.graph.agent_graph import AgentGraph
from src.utils.retriever import WeaviateRetriever
from src.utils.generator import OpenAIGenerator

class AgenticRunner:
    def __init__(self, retriever=None, generator=None):
        self.retriever = retriever or WeaviateRetriever()
        self.generator = generator or OpenAIGenerator()

        self.graph = AgentGraph(
            retriever=self.retriever,
            generator=self.generator
        )

    def run(self, question: str) -> dict:
        try:
            return self.graph.run(question)
        except Exception as e:
            return {
                "answer": f"❌ Error while running agent: {str(e)}",
                "grounding": []
            }
