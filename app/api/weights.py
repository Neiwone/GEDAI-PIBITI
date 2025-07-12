from typing import Annotated
from fastapi import Body, APIRouter
from app.schemas.weight_input import CalculateAHPWeightsDTO, CalculateBWMWeightsDTO
from app.core.methods import calculate_weights

router = APIRouter(
    prefix="/weights",
    tags=["Weights"]
)

@router.post(
    "/ahp",
    response_model=dict,
    status_code=201,
    summary="Retrieve criterion weights from AHP method"
)
async def get_ahp_weights(request: Annotated[CalculateAHPWeightsDTO, Body(embed=True)]):
    '''
    Get list of the proposed weights by AHP method
    '''
    try:
        weights = calculate_weights(request)
        return {"weights": weights}
    except ValueError as e:
        raise e


@router.post(
    "/bwm",
    response_model=dict,
    status_code=201,
    summary="Retrieve criterion weights from BWM method"
)
async def get_bwm_weights(request: Annotated[CalculateBWMWeightsDTO, Body(embed=True)]):
    '''
    Get list of the proposed weights by Best-Worst method
    '''
    try:
        weights = calculate_weights(request)
        return {"weights": weights}
    except ValueError as e:
        raise e