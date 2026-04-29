from app.rag.pipeline import RAGPipeline

if __name__ == "__main__":
    rag = RAGPipeline()

    while True:
        query = input("\nAsk a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        result = rag.run(query)

        print("\nAnswer:")
        print(result["answer"])
