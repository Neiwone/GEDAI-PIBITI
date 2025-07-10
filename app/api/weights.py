from fastapi import APIRouter, HTTPException
from app.models.weight_input import AHPRequest, BWRequest
from app.core.methods import calculate_weights

router = APIRouter()

@router.post("/ahp_weights")
def get_ahp_weights(request: AHPRequest):
    try:
        weights = calculate_weights(request)
        return {"criteria": request.criteria, "weights": weights}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bwm_weights")
def get_bwm_weights(request: BWRequest):
    try:
        weights = calculate_weights(request)
        return {"criteria": request.criteria, "weights": weights}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))