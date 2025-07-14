from pydantic import BaseModel
from typing import Optional, List

from app.schemas.alternative import AlternativeReadShort
from app.schemas.criterion import CriterionCreate, CriterionReadShort


class EvaluationBase(BaseModel):
    name: str
    description: Optional[str] = None


class EvaluationCreate(EvaluationBase):
    criteria: List[CriterionCreate]


class EvaluationRead(EvaluationBase):
    id: int
    alternatives: List[AlternativeReadShort] = []
    criteria: List[CriterionReadShort] = []

    class Config:
        from_attributes=True
