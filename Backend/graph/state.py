from typing import TypedDict, Optional
from langchain_core.messages import BaseMessage


class GraphState(TypedDict, total=False):
    """State shared across all agents in the procurement workflow."""

    # --- Request identification ---
    employee: str                          # Employee name
    employee_id: Optional[int]             # Employee ID for tool lookups
    department_id: Optional[int]           # Department the employee belongs to

    # --- Item details ---
    item: str                              # Item name/description
    item_id: Optional[int]                 # Stationary item ID
    quantity: int                          # Requested quantity
    price: float                           # Unit price
    total_cost: float                      # quantity * price (computed once)

    # --- Vendor ---
    vendor: str                            # Vendor name
    vendor_id: Optional[int]              # Vendor ID for tool lookups

    # --- Workflow decisions ---
    approved: bool                         # Final approval status
    status: str                            # pending | approved | rejected | ordered
    risk_level: str                        # low | medium | high
    human_approval_required: bool          # Whether human review is needed
    policy_compliant: bool                 # Whether it passes policy checks
    budget_sufficient: bool                # Whether budget covers the cost

    # --- Output ---
    purchase_order_id: Optional[int]       # ID of the created purchase order
    comments: str                          # Running comments/explanations
    notification: str                      # Final notification message

    # --- LLM conversation (optional, for LangGraph message passing) ---
    messages: list[BaseMessage]


# Node name constants
GraphState.REQUEST_PARSER = "request_parser"
GraphState.BUDGET_VERIFICATION = "budget_verification"
GraphState.RISK_ASSESSMENT = "risk_assessment"
GraphState.POLICY_CHECKER = "policy_checker"
GraphState.HUMAN_APPROVAL = "human_approval"
GraphState.VENDOR_RECOMMENDATION = "vendor_recommendation"
GraphState.PURCHASE_ORDER = "purchase_order"
GraphState.NOTIFICATION = "notification"
