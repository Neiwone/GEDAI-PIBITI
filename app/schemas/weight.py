from pydantic import BaseModel, Field
from typing import List

class CalculateAHPWeights(BaseModel):
    criteria: List[str] = Field(default=["Cost", "Inovation", "Tecnology", "Management", "Market"])
    matrix: List[List[float]] = Field(
        default=[
            [1, 1/3, 1/5, 1, 1/4],
            [3, 1, 1/2, 2, 1/3],
            [5, 2, 1, 4, 5],
            [1, 1/2, 1/4, 1, 1/4],
            [4, 3, 1/5, 4, 1]
            ])

class CalculateBWMWeights(BaseModel):
    criteria: List[str] = Field(default=["Cost", "Inovation", "Tecnology", "Management", "Market"])
    most_important: List[float] = Field(default=[2, 1, 4, 3, 8])
    least_important: List[float] = Field(default=[4, 8, 2, 3, 1])
