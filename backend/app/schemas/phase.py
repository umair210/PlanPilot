from pydantic import BaseModel


class PhaseRead(BaseModel):
    id: str
    goal_id: str
    title: str
    objective: str
    order_index: int

    class Config:
        from_attributes = True
