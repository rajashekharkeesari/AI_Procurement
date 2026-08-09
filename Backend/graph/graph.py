from langgraph.constants import START, END
from langgraph.graph import StateGraph
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
workflow.add_node(request_parser_agent)
workflow.add_node(Budget_verification_agent)
workflow.add_node(risk_assessment_agent)
workflow.add_node(policy_checker_agent)
workflow.add_node(Human_approval_agent)
workflow.add_node(vendor_recommendation_agent)
workflow.add_node(purchase_order_agent)

workflow.add_edge(START, "request_parser_agent")
workflow.add_edge("request_parser_agent", "Budget_verification_agent")
workflow.add_edge("Budget_verification_agent", "risk_assessment_agent")
workflow.add_edge("risk_assessment_agent", "policy_checker_agent")
workflow.add_edge("policy_checker_agent", "Human_approval_agent")
workflow.add_edge("Human_approval_agent", "vendor_recommendation_agent")
workflow.add_edge("vendor_recommendation_agent", "purchase_order_agent")
workflow.add_edge("purchase_order_agent", END)

workflow.set_entry_point("request_parser_agent")
workflow.set_finish_point("purchase_order_agent")

compiled_workflow = workflow.compile()
