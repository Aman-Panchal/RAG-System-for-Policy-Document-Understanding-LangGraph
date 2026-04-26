from app.rag.pipeline import RAGPipeline
from app.tools.email_tool import email_tool
from app.core.logging import logger

rag = RAGPipeline()


def retrieve_node(state: dict):
    query = state["query"]

    logger.info(f"Received query: {query}")

    result = rag.run(query)

    logger.info("Generated response")

    return {
        **state,
        "answer": result["answer"],
        "sources": result["sources"]
    }

def decision_node(state: dict):
    answer = state["answer"]

    if "I don't know" in answer:
        return "needs_human"

    # Only act if frontend explicitly says so
    if state.get("send_email") and state.get("user_email"):
        return "send_email"

    return "end"

def email_node(state: dict):
    logger.info(f"Sending email to {state.get('user_email')}")
    result = email_tool(state)

    logger.info(f"Email status: {result.get('email_status')}")

    return result
    
    
def detect_email_intent(state: dict):
    query = state["query"]

    # Simple heuristic (we can later replace with LLM)
    keywords = ["send", "email", "mail", "share"]

    if any(word in query.lower() for word in keywords):
        return {**state, "email_intent": True}

    return {**state, "email_intent": False}


def hitl_node(state: dict):
    """
    This node simulates asking user for approval.
    In real UI (Streamlit), this will be interactive.
    """
    print("\n⚠️ Do you want to send this response to your email? (y/n)")
    user_input = input().lower()

    if user_input == "y":
        email = input("Enter your email: ")
        return {
            **state,
            "send_email": True,
            "user_email": email
        }

    return {
        **state,
        "send_email": False
    }
