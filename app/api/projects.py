from typing import List
from fastapi import APIRouter, HTTPException, Path

from app.schemas.evaluation import Evaluation, EvaluationCreate
from app.schemas.alternative import AlternativeCreate
from app.schemas.criterion import CriterionCreate

# TODO: CHANGE THIS IN NEXT UPDATE
fake_db: List[Evaluation] = []
current_id = 0

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# Endpoint to create a new evaluation
@router.post(
    "/",
    response_model=Evaluation,
    status_code=201,
    summary="Create a new evaluation project"
)
async def create_evaluation(evaluation_data: EvaluationCreate):
    '''
    Create a new evaluation project with a name, description,
    and initial lists of alternatives and criteria.
    '''
    global current_id
    current_id += 1
    
    new_alternatives = []
    for i, alt_data in enumerate(evaluation_data.alternatives):
        new_alternatives.append(
            {**alt_data.model_dump(), "id": i + 1}
        )

    new_criteria = []
    for i, crit_data in enumerate(evaluation_data.criteria):
        new_criteria.append(
            {**crit_data.model_dump(), "id": i + 1}
        )

    new_evaluation = Evaluation(
        id=current_id,
        name=evaluation_data.name,
        description=evaluation_data.description,
        alternatives=new_alternatives,
        criteria=new_criteria
    )
    fake_db.append(new_evaluation)
    return new_evaluation

# Endpoint to get a list of all evaluations
@router.get(
    "/",
    response_model=List[Evaluation],
    summary="Retrieve all evaluation projects"
)
async def get_all_evaluations():
    '''
    Get a list of all evaluation projects stored in the system.
    '''
    return fake_db

# Endpoint to get a single evaluation by ID
@router.get(
    "/{evaluation_id}",
    response_model=Evaluation,
    summary="Retrieve a specific evaluation project by ID"
)
async def get_evaluation(
    evaluation_id: int = Path(..., description="The ID of the evaluation project")
):
    '''
    Get the details of a single evaluation project, including its alternatives and criteria.
    '''
    for evaluation in fake_db:
        if evaluation.id == evaluation_id:
            return evaluation
    raise HTTPException(status_code=404, detail="Evaluation not found")

# Endpoint to delete an evaluation by ID
@router.delete(
    "/{evaluation_id}",
    status_code=204,
    summary="Delete an evaluation project"
)
async def delete_evaluation(
    evaluation_id: int = Path(..., description="The ID of the evaluation project to delete")
):
    '''
    Delete an evaluation project and all its associated data.
    '''
    global fake_db
    initial_len = len(fake_db)
    fake_db = [eval for eval in fake_db if eval.id != evaluation_id]
    if len(fake_db) == initial_len:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return {"message": "Evaluation deleted successfully"}

# Endpoint to update an evaluation
@router.put(
    "/{evaluation_id}",
    response_model=Evaluation,
    summary="Update an entire evaluation project"
)
async def update_evaluation(
    evaluation_id: int,
    evaluation_data: EvaluationCreate
):
    for i, evaluation in enumerate(fake_db):
        if evaluation.id == evaluation_id:
            updated_evaluation = Evaluation(
                id=evaluation_id,
                **evaluation_data.model_dump()
            )
            fake_db[i] = updated_evaluation
            return updated_evaluation
    raise HTTPException(status_code=404, detail="Evaluation not found")


# Endpoints for managing alternatives and criteria within a project
@router.post(
    "/{evaluation_id}/alternatives/",
    response_model=AlternativeCreate,
    status_code=201,
    summary="Add an alternative to a project"
)
async def add_alternative(
    evaluation_id: int,
    alternative: AlternativeCreate
):
    for eval in fake_db:
        if eval.id == evaluation_id:
            return alternative
    raise HTTPException(status_code=404, detail="Evaluation not found")

@router.post(
    "/{evaluation_id}/criteria/",
    response_model=CriterionCreate,
    status_code=201,
    summary="Add a criterion to a project"
)
async def add_criterion(
    evaluation_id: int,
    criterion: CriterionCreate
):
    for eval in fake_db:
        if eval.id == evaluation_id:
            return criterion
    raise HTTPException(status_code=404, detail="Evaluation not found")