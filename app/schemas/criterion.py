from pydantic import BaseModel
from typing import Optional


class CriterionBase(BaseModel):
    name: str
    description: Optional[str] = None
    weight: Optional[float] = None


class CriterionCreate(CriterionBase):
    pass


class CriterionRead(CriterionBase):
    id: int
    evaluation_id: int

    class Config:
        from_attributes=True


class CriterionReadShort(CriterionBase):
    name: str

    class Config:
        from_attributes=True
