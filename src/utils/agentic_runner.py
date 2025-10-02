# src/utils/agentic_runner.py

import os
from src.graph.agent_graph import AgentGraph
from src.utils.retriever import WeaviateRetriever
from src.utils.generator import OpenAIGenerator


class AgenticRunner:
    """
    Orchestrates the agent pipeline using LangGraph.
    Components:
    - Retriever: pulls relevant transcript chunks from Weaviate
    - Generator: uses OpenAI to ground answers with citations
    - Graph: connects these into an agent flow
    """

    def __init__(self):
        # Initialize building blocks
        self.retriever = WeaviateRetriever()
        self.generator = OpenAIGenerator()

        # Build LangGraph app
        self.graph = AgentGraph(
            retriever=self.retriever,
            generator=self.generator
        )

    def run(self, question: str) -> dict:
        """
        Run a full agentic cycle:
        1. Retrieve top-k chunks from Weaviate
        2. Generate grounded answer with citations
        Returns structured dict {answer, grounding}
        """
        try:
            result = self.graph.run(question)
            return result
        except Exception as e:
            return {
                "answer": f"❌ Error while running agent: {str(e)}",
                "grounding": []
            }
