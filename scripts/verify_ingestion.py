# scripts/verify_ingestion.py
import os
import weaviate

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
CLASS_NAME = "KnowledgeChunk"

def main():
    client = weaviate.Client(WEAVIATE_URL)

    # --- Check schema ---
    schema = client.schema.get()
    classes = [c["class"] for c in schema["classes"]]
    print("\n=== Schema Classes ===")
    print(classes)

    if CLASS_NAME not in classes:
        print(f"❌ No class '{CLASS_NAME}' found in Weaviate")
        return

    # --- Count objects ---
    query = (
        client.query
        .aggregate(CLASS_NAME)
        .with_meta_count()
        .do()
    )
    count = query["data"]["Aggregate"][CLASS_NAME][0]["meta"]["count"]
    print(f"\n=== Total {CLASS_NAME} Objects: {count} ===")

    # --- Fetch a few objects ---
    print("\n=== Sample Objects ===")
    res = (
        client.query
        .get(CLASS_NAME, ["title", "text", "start_time", "end_time"])
        .with_limit(5)
        .do()
    )
    for obj in res["data"]["Get"][CLASS_NAME]:
        title = obj.get("title")
        text = obj.get("text")
        st = obj.get("start_time", "?")
        et = obj.get("end_time", "?")
        print(f"[{title} {st}–{et}] {text[:100]}...")

if __name__ == "__main__":
    main()
