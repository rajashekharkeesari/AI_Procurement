"""
Workflow Routes

Exposes API endpoints to:
1. Start a procurement workflow (/run)
2. Resume a paused workflow after human approval (/resume)
3. Check workflow status (/status/{thread_id})
"""

import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from langgraph.types import Command

from Backend.graph.graph import compiled_workflow


class WorkflowRequest(BaseModel):
    employee: str = Field(..., example="Alice")
    item: str = Field(..., example="Laptop")
    quantity: int = Field(..., example=2)
    price: float = Field(..., example=1200.0)
    vendor: str = Field("", example="Acme Supplies")


class ApprovalDecision(BaseModel):
    thread_id: str = Field(..., example="abc-123")
    approved: bool = Field(..., example=True)
    comment: str = Field("", example="Looks good, approved.")


router = APIRouter()


@router.post("/run")
def run_workflow(payload: WorkflowRequest):
    """
    Start a new procurement workflow.

    Returns:
    - If the workflow completes without interruption: full result.
    - If the workflow pauses at human approval: thread_id + approval summary.
    """
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "employee": payload.employee,
        "item": payload.item,
        "quantity": payload.quantity,
        "price": payload.price,
        "vendor": payload.vendor,
        "approved": False,
        "status": "pending",
        "comments": "",
    }

    try:
        # invoke runs until completion or until an interrupt is hit
        result = compiled_workflow.invoke(initial_state, config=config)

        # After invoke, check if the graph is actually paused at an interrupt
        graph_state = compiled_workflow.get_state(config)

        if graph_state and graph_state.next:
            # Workflow is paused — extract interrupt data
            interrupt_value = None
            if hasattr(graph_state, "tasks") and graph_state.tasks:
                for task in graph_state.tasks:
                    if hasattr(task, "interrupts") and task.interrupts:
                        interrupt_value = task.interrupts[0].value
                        break

            return {
                "success": True,
                "completed": False,
                "waiting_for": "human_approval",
                "thread_id": thread_id,
                "approval_summary": interrupt_value,
                "current_state": graph_state.values,
                "message": "Workflow paused. Send approval decision to /resume.",
            }

        # Workflow completed fully
        return {
            "success": True,
            "completed": True,
            "thread_id": thread_id,
            "workflow_state": result,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/resume")
def resume_workflow(decision: ApprovalDecision):
    """
    Resume a paused workflow with the human approval decision.

    The frontend sends the thread_id and the approve/reject decision.
    The workflow continues from where it was interrupted.
    """
    config = {"configurable": {"thread_id": decision.thread_id}}

    # Verify the workflow is actually paused
    state = compiled_workflow.get_state(config)

    if not state or not state.next:
        raise HTTPException(
            status_code=400,
            detail="No paused workflow found for this thread_id.",
        )

    try:
        # Resume the workflow by sending the human decision
        result = compiled_workflow.invoke(
            Command(resume={"approved": decision.approved, "comment": decision.comment}),
            config=config,
        )

        return {
            "success": True,
            "completed": True,
            "thread_id": decision.thread_id,
            "workflow_state": result,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/status/{thread_id}")
def get_workflow_status(thread_id: str):
    """
    Check the status of a workflow by thread_id.

    Returns the current state and whether it's waiting for input.
    """
    config = {"configurable": {"thread_id": thread_id}}

    state = compiled_workflow.get_state(config)

    if not state:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found.",
        )

    is_paused = bool(state.next)

    interrupt_value = None
    if is_paused and hasattr(state, "tasks") and state.tasks:
        for task in state.tasks:
            if hasattr(task, "interrupts") and task.interrupts:
                interrupt_value = task.interrupts[0].value
                break

    return {
        "thread_id": thread_id,
        "paused": is_paused,
        "waiting_at": list(state.next) if state.next else [],
        "approval_summary": interrupt_value,
        "current_state": state.values,
    }
