from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.schemas.evaluation import EvaluationRead, EvaluationCreate
from app.schemas.alternative import AlternativeCreateShort, AlternativeCreate, AlternativeRead
from app.db.database import get_db
from app.core.models import Evaluation as DBEvaluation, Alternative as DBAlternative, Criterion as DBCriterion

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post(
    "/",
    response_model=EvaluationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new evaluation project"
)
async def create_evaluation(evaluation_data: EvaluationCreate, db: AsyncSession = Depends(get_db)):
    db_evaluation = DBEvaluation(name=evaluation_data.name, description=evaluation_data.description)
    db.add(db_evaluation)
    await db.flush()

    for crit_data in evaluation_data.criteria:
        db.add(DBCriterion(**crit_data.model_dump(), evaluation_id=db_evaluation.id))

    await db.commit()
    await db.refresh(db_evaluation)

    result = await db.execute(
        select(DBEvaluation).where(DBEvaluation.id == db_evaluation.id)
        .options(selectinload(DBEvaluation.alternatives), selectinload(DBEvaluation.criteria))
    )
    full_db_evaluation = result.scalars().first()
    return EvaluationRead.model_validate(full_db_evaluation)

@router.get(
    "/",
    response_model=List[EvaluationRead],
    summary="Retrieve all evaluation projects"
)
async def get_all_evaluations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DBEvaluation).options(selectinload(DBEvaluation.alternatives), selectinload(DBEvaluation.criteria))
    )
    evaluations = result.scalars().all()
    return [EvaluationRead.model_validate(eval) for eval in evaluations]

@router.get(
    "/{evaluation_id}",
    response_model=EvaluationRead,
    summary="Retrieve a specific evaluation project by ID"
)
async def get_evaluation(evaluation_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DBEvaluation).where(DBEvaluation.id == evaluation_id)
        .options(selectinload(DBEvaluation.alternatives), selectinload(DBEvaluation.criteria))
    )
    evaluation = result.scalars().first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")
    return EvaluationRead.model_validate(evaluation)

@router.delete(
    "/{evaluation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an evaluation project"
)
async def delete_evaluation(evaluation_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBEvaluation).where(DBEvaluation.id == evaluation_id))
    evaluation = result.scalars().first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")
    await db.delete(evaluation)
    await db.commit()
    return {"message": "Evaluation deleted successfully"}



@router.put(
    "/{evaluation_id}",
    response_model=EvaluationRead,
    summary="Update an entire evaluation project"
)
async def update_evaluation(evaluation_id: int, evaluation_data: EvaluationCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DBEvaluation).where(DBEvaluation.id == evaluation_id)
        .options(selectinload(DBEvaluation.alternatives), selectinload(DBEvaluation.criteria))
    )
    db_evaluation = result.scalars().first()
    if not db_evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")

    db_evaluation.name = evaluation_data.name # type: ignore
    db_evaluation.description = evaluation_data.description # type: ignore

    await db.execute(delete(DBCriterion).where(DBCriterion.evaluation_id == evaluation_id))
    await db.flush()

    for crit_data in evaluation_data.criteria:
        db.add(DBCriterion(**crit_data.model_dump(), evaluation_id=evaluation_id))

    await db.commit()
    await db.refresh(db_evaluation)

    result = await db.execute(
        select(DBEvaluation).where(DBEvaluation.id == evaluation_id)
        .options(selectinload(DBEvaluation.alternatives), selectinload(DBEvaluation.criteria))
    )
    updated_evaluation = result.scalars().first()
    return EvaluationRead.model_validate(updated_evaluation)

@router.post(
    "/{evaluation_id}/alternatives/",
    response_model=AlternativeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add an alternative to a project"
)
async def add_alternative(evaluation_id: int, alternative: AlternativeCreateShort, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DBEvaluation).where(DBEvaluation.id == evaluation_id)
    )
    evaluation = result.scalars().first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")

    new_alternative = AlternativeCreate(title=alternative.title, description=alternative.description, proposer=alternative.proposer, evaluation_id=evaluation_id)
    db_alternative = DBAlternative(**new_alternative.model_dump())

    db.add(db_alternative)
    await db.commit()

    result = await db.execute(
        select(DBAlternative).options(selectinload(DBAlternative.notes)).where(DBAlternative.id == db_alternative.id)
    )
    db_alternative = result.scalars().first()

    return AlternativeRead.model_validate(db_alternative, from_attributes=True)
