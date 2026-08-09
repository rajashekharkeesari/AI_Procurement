from typing import TypedDict

class GraphState(TypedDict):
    employee: str
    item: str
    quantity: int
    price: float
    vendor: str
    approved: bool
    comments: str

GraphState.REQUEST_PARSER = "request_parser"
GraphState.BUDGET_VERIFICATION = "budget_verification"
GraphState.RISK_ASSESSMENT = "risk_assessment"
GraphState.POLICY_CHECKER = "policy_checker"
GraphState.HUMAN_APPROVAL = "human_approval"
GraphState.VENDOR_RECOMMENDATION = "vendor_recommendation"
GraphState.PURCHASE_ORDER = "purchase_order"