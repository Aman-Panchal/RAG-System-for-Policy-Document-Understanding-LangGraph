from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.graph.nodes import (
    retrieve_node,
    decision_node,
    email_node,
    detect_email_intent,
    hitl_node
)

class GraphState(TypedDict):
    query: str
    answer: str
    sources: list
    send_email: bool
    user_email: str
    email_status: str
    email_intent: bool


def build_graph():
    workflow = StateGraph(GraphState)

    # Nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("intent", detect_email_intent)
    workflow.add_node("decision", decision_node)
    workflow.add_node("hitl", hitl_node)
    workflow.add_node("email", email_node)

    # Flow
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "intent")
    workflow.add_edge("intent", "decision")

    workflow.add_conditional_edges(
        "decision",
        decision_node,
        {
            "needs_human": END,
            "hitl": "hitl",
            "send_email": "email",
            "end": END
        }
    )

    workflow.add_edge("hitl", "decision")
    workflow.add_edge("email", END)

    return workflow.compile()
