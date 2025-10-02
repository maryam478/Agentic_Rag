from src.utils.retriever import WeaviateRetriever
from src.utils.generator import OpenAIGenerator

retriever = WeaviateRetriever()
generator = OpenAIGenerator()

def retrieve_node(state):
    """Retrieve relevant context from Weaviate."""
    hits = retriever.retrieve(state["question"])
    state["hits"] = hits
    return state

def reasoning_node(state):
    """Optional reasoning step."""
    if not state.get("hits"):
        state["notes"] = "No context found, fallback to 'I don't know'."
    else:
        state["notes"] = f"Retrieved {len(state['hits'])} chunks."
    return state

def generate_node(state):
    """Generate final grounded answer."""
    state["response"] = generator.generate(
        state["question"], state.get("hits", [])
    )
    return state

