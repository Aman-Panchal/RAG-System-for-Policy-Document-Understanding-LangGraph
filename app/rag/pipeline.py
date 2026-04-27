from app.rag.retriever import get_retriever
from app.rag.generator import get_llm, get_prompt


class RAGPipeline:
    def __init__(self):
        self.retriever = get_retriever()
        self.llm = get_llm()
        self.prompt = get_prompt()

    def format_docs(self, docs):
        return "\n\n".join([doc.page_content for doc in docs])

    def run(self, query: str):
        # Step 1: Retrieve
        docs = self.retriever.get_relevant_documents(query)

        # Step 2: Format context
        context = self.format_docs(docs)

        # Step 3: Create prompt
        prompt = self.prompt.format(
            context=context,
            question=query
        )

        # Step 4: Generate response
        response = self.llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": docs
        }
