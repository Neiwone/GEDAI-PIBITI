from fastapi import Body, APIRouter, HTTPException
from typing import Annotated
from app.models.weight_input import CalculateAHPWeightsDTO, CalculateBWMWeightsDTO
from app.core.methods import calculate_weights

router = APIRouter()

@router.post("/ahp_weights")
def get_ahp_weights(request: Annotated[CalculateAHPWeightsDTO, Body(embed=True)]):
    try:
        weights = calculate_weights(request)
        return {"criteria": request.criteria, "weights": weights}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bwm_weights")
def get_bwm_weights(request: Annotated[CalculateBWMWeightsDTO, Body(embed=True)]):
    try:
        weights = calculate_weights(request)
        return {"criteria": request.criteria, "weights": weights}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))