from typing import List
from pydantic import BaseModel
from app.schemas.alternative import Alternative, AlternativeCreate
from app.schemas.criterion import Criterion, CriterionCreate

class EvaluationBase(BaseModel):
    name: str
    description: str | None = None

class EvaluationCreate(EvaluationBase):
    alternatives: List[AlternativeCreate]
    criteria: List[CriterionCreate]

class Evaluation(EvaluationBase):
    id: int
    alternatives: List[Alternative] = []
    criteria: List[Criterion] = []

    class Config:
        from_attributes = True