from pydantic import BaseModel

class CriterionBase(BaseModel):
    name: str
    description: str | None = None

class CriterionCreate(CriterionBase):
    pass

class Criterion(CriterionBase):
    id: int
    weight: float | None = None

    class Config:
        from_attributes = True