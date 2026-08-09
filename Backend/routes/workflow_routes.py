from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from Backend.graph.graph import compiled_workflow


class WorkflowState(BaseModel):
    employee: str = Field(..., example="Alice")
    item: str = Field(..., example="Laptop")
    quantity: int = Field(..., example=2)
    price: float = Field(..., example=1200.0)
    vendor: str = Field("", example="Acme Supplies")
    approved: bool = Field(False, example=False)
    comments: str = Field("", example="")


router = APIRouter()


@router.post("/run")
def run_workflow(payload: WorkflowState):
    try:
        result = compiled_workflow.invoke(payload.dict())
        return {"success": True, "workflow_state": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
