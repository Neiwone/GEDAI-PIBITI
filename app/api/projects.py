from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.schemas.evaluation import Evaluation, EvaluationCreate
from app.schemas.alternative import AlternativeCreate
from app.schemas.criterion import CriterionCreate
from app.db.database import get_db
from app.core.models import Evaluation as DBEvaluation, Alternative as DBAlternative, Criterion as DBCriterion

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post(
    "/",
    response_model=Evaluation,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new evaluation project"
)
async def create_evaluation(
    evaluation_data: EvaluationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new evaluation project with a name, description,
    and initial lists of alternatives and criteria.
    """
    db_evaluation = DBEvaluation(
        name=evaluation_data.name,
        description=evaluation_data.description,
        # created_by_user_id foi removido
    )
    db.add(db_evaluation)
    await db.flush() # Para obter o ID do db_evaluation antes de comitar

    for alt_data in evaluation_data.alternatives:
        db_alternative = DBAlternative(**alt_data.model_dump(), evaluation_id=db_evaluation.id)
        db.add(db_alternative)

    for crit_data in evaluation_data.criteria:
        db_criterion = DBCriterion(**crit_data.model_dump(), evaluation_id=db_evaluation.id)
        db.add(db_criterion)

    await db.commit()
    await db.refresh(db_evaluation) # Atualiza o objeto com os dados do DB

    # Carregar as relações para o retorno do Pydantic
    result = await db.execute(
        select(DBEvaluation)
        .where(DBEvaluation.id == db_evaluation.id)
        .options(
            selectinload(DBEvaluation.alternatives),
            selectinload(DBEvaluation.criteria)
        )
    )
    full_db_evaluation = result.scalars().first()
    if not full_db_evaluation:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve created evaluation.")
    return Evaluation.model_validate(full_db_evaluation)

@router.get(
    "/",
    response_model=List[Evaluation],
    summary="Retrieve all evaluation projects"
)
async def get_all_evaluations(
    db: AsyncSession = Depends(get_db),
):
    """
    Get a list of all evaluation projects stored in the system.
    """
    result = await db.execute(
        select(DBEvaluation)
        .options(
            selectinload(DBEvaluation.alternatives),
            selectinload(DBEvaluation.criteria)
        )
    )
    evaluations = result.scalars().all()
    return [Evaluation.model_validate(eval) for eval in evaluations]

@router.get(
    "/{evaluation_id}",
    response_model=Evaluation,
    summary="Retrieve a specific evaluation project by ID"
)
async def get_evaluation(
    evaluation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get the details of a single evaluation project, including its alternatives and criteria.
    """
    result = await db.execute(
        select(DBEvaluation)
        .where(DBEvaluation.id == evaluation_id)
        .options(
            selectinload(DBEvaluation.alternatives),
            selectinload(DBEvaluation.criteria)
        )
    )
    evaluation = result.scalars().first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")
    return Evaluation.model_validate(evaluation)

@router.delete(
    "/{evaluation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an evaluation project"
)
async def delete_evaluation(
    evaluation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an evaluation project and all its associated data.
    """
    result = await db.execute(
        select(DBEvaluation)
        .where(DBEvaluation.id == evaluation_id)
    )
    evaluation = result.scalars().first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")

    await db.delete(evaluation)
    await db.commit()
    return {"message": "Evaluation deleted successfully"}

@router.put(
    "/{evaluation_id}",
    response_model=Evaluation,
    summary="Update an entire evaluation project"
)
async def update_evaluation(
    evaluation_id: int,
    evaluation_data: EvaluationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an entire evaluation project.
    """
    result = await db.execute(
        select(DBEvaluation)
        .where(DBEvaluation.id == evaluation_id)
        .options(
            selectinload(DBEvaluation.alternatives),
            selectinload(DBEvaluation.criteria)
        )
    )
    db_evaluation = result.scalars().first()
    if not db_evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")

    db_evaluation.name = evaluation_data.name # type: ignore
    db_evaluation.description = evaluation_data.description # type: ignore

    # Lógica para atualizar alternativas e critérios:
    await db.execute(delete(DBAlternative).where(DBAlternative.evaluation_id == evaluation_id))
    await db.execute(delete(DBCriterion).where(DBCriterion.evaluation_id == evaluation_id))
    await db.flush()

    for alt_data in evaluation_data.alternatives:
        db.add(DBAlternative(**alt_data.model_dump(), evaluation_id=evaluation_id))
    for crit_data in evaluation_data.criteria:
        db.add(DBCriterion(**crit_data.model_dump(), evaluation_id=evaluation_id))

    await db.commit()
    await db.refresh(db_evaluation)

    result = await db.execute(
        select(DBEvaluation)
        .where(DBEvaluation.id == evaluation_id)
        .options(
            selectinload(DBEvaluation.alternatives),
            selectinload(DBEvaluation.criteria)
        )
    )
    updated_evaluation = result.scalars().first()
    return Evaluation.model_validate(updated_evaluation)


@router.post(
    "/{evaluation_id}/alternatives/",
    response_model=AlternativeCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Add an alternative to a project"
)
async def add_alternative(
    evaluation_id: int,
    alternative: AlternativeCreate,
    db: AsyncSession = Depends(get_db),
):
    # Verifica se o projeto existe
    result = await db.execute(
        select(DBEvaluation)
        .where(DBEvaluation.id == evaluation_id)
    )
    evaluation = result.scalars().first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")

    db_alternative = DBAlternative(**alternative.model_dump(), evaluation_id=evaluation_id)
    db.add(db_alternative)
    await db.commit()
    await db.refresh(db_alternative)
    return alternative

@router.post(
    "/{evaluation_id}/criteria/",
    response_model=CriterionCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Add a criterion to a project"
)
async def add_criterion(
    evaluation_id: int,
    criterion: CriterionCreate,
    db: AsyncSession = Depends(get_db),
):
    # Verifica se o projeto existe
    result = await db.execute(
        select(DBEvaluation)
        .where(DBEvaluation.id == evaluation_id)
    )
    evaluation = result.scalars().first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")

    db_criterion = DBCriterion(**criterion.model_dump(), evaluation_id=evaluation_id)
    db.add(db_criterion)
    await db.commit()
    await db.refresh(db_criterion)
    return criterion