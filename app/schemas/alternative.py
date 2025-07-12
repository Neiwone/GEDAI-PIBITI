from pydantic import BaseModel

class AlternativeBase(BaseModel):
    title: str
    description: str | None = None
    proposer: str

class AlternativeCreate(AlternativeBase):
    pass

class Alternative(AlternativeBase):
    id: int

    class Config:
        from_attributes = True