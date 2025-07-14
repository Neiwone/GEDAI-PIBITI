from pydantic import BaseModel
from typing import Optional, List


class AlternativeCriterionNoteBase(BaseModel):
    note: float


class AlternativeCriterionNoteCreate(AlternativeCriterionNoteBase):
    alternative_id: int
    criterion_id: int


class AlternativeCriterionNoteRead(AlternativeCriterionNoteBase):
    id: int
    alternative_id: int
    criterion_id: int

    class Config:
        from_attributes = True


class AlternativeBase(BaseModel):
    title: str
    description: Optional[str] = None
    proposer: Optional[str] = None


class AlternativeCreateShort(AlternativeBase):
    pass

class AlternativeCreate(AlternativeBase):
    evaluation_id: int


class AlternativeRead(AlternativeBase):
    id: int
    evaluation_id: int
    notes: List[AlternativeCriterionNoteRead] = []

    class Config:
        from_attributes = True


class AlternativeReadShort(AlternativeBase):
    id: int

    class Config:
        from_attributes = True
