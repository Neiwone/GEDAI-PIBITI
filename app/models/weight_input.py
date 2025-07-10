from pydantic import BaseModel
from typing import List

class AHPRequest(BaseModel):
    criteria: List[str] 
    matrix: List[List[float]]

class BWRequest(BaseModel):
    criteria: List[str] 
    most_important: List[float]
    least_important: List[float]
