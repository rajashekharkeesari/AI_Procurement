from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from .state import GraphState
from Backend.agents import (
    Budget_verification_agent,
    Human_approval_agent,
    notification_agent,
    policy_checker_agent,
    purchase_order_agent,
    request_parser_agent,
    risk_assessment_agent,
    vendor_recommendation_agent,
)

workflow = StateGraph(GraphState)

# Add all nodes
workflow.add_node("request_parser", request_parser_agent)
workflow.add_node("budget_verification", Budget_verification_agent)
workflow.add_node("risk_assessment", risk_assessment_agent)
workflow.add_node("policy_checker", policy_checker_agent)
workflow.add_node("human_approval", Human_approval_agent)
workflow.add_node("vendor_recommendation", vendor_recommendation_agent)
workflow.add_node("purchase_order", purchase_order_agent)
workflow.add_node("notification", notification_agent)

# Define edges
workflow.add_edge(START, "request_parser")
workflow.add_edge("request_parser", "budget_verification")
workflow.add_edge("budget_verification", "risk_assessment")
workflow.add_edge("risk_assessment", "policy_checker")
workflow.add_edge("policy_checker", "human_approval")
workflow.add_edge("human_approval", "vendor_recommendation")
workflow.add_edge("vendor_recommendation", "purchase_order")
workflow.add_edge("purchase_order", "notification")
workflow.add_edge("notification", END)

# Persistent SQLite checkpointer — survives server restarts
import sqlite3
_conn = sqlite3.connect("./workflow_checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=_conn)

compiled_workflow = workflow.compile(checkpointer=checkpointer)
