# src/graph/agent_graph.py

from langgraph.graph import StateGraph


class AgentGraph:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator

        # Build simple state graph
        self.graph = StateGraph(dict)

        self.graph.add_node("retrieve", self._retrieve)
        self.graph.add_node("generate", self._generate)

        self.graph.set_entry_point("retrieve")
        self.graph.add_edge("retrieve", "generate")
        self.graph.set_finish_point("generate")

        self.app = self.graph.compile()

    def _retrieve(self, state: dict):
        hits = self.retriever.retrieve(state["input"], top_k=5)
        return {"hits": hits, "input": state["input"]}

    def _generate(self, state: dict):
        answer = self.generator.generate(state["input"], state["hits"])
        return {"answer": answer, "grounding": state["hits"]}

    def run(self, question: str) -> dict:
        return self.app.invoke({"input": question})
