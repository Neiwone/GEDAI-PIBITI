from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Modelo para Avaliações/Projetos
class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)

    alternatives = relationship("Alternative", back_populates="evaluation", cascade="all, delete-orphan")
    criteria = relationship("Criterion", back_populates="evaluation", cascade="all, delete-orphan")
    submissions = relationship("EvaluationSubmission", back_populates="evaluation", cascade="all, delete-orphan")

# Modelo para Alternativas
class Alternative(Base):
    __tablename__ = "alternatives"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    proposer = Column(String)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))

    evaluation = relationship("Evaluation", back_populates="alternatives")

# Modelo para Critérios
class Criterion(Base):
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    weight = Column(Float, nullable=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))

    evaluation = relationship("Evaluation", back_populates="criteria")
    submission_scores = relationship("SubmissionScore", back_populates="criterion", cascade="all, delete-orphan")

# Modelo para Submissões de Avaliação
class EvaluationSubmission(Base):
    __tablename__ = "evaluation_submissions"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    comments = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    evaluation = relationship("Evaluation", back_populates="submissions")
    scores = relationship("SubmissionScore", back_populates="submission", cascade="all, delete-orphan")

# Modelo para as Notas Individuais dentro de uma Submissão
class SubmissionScore(Base):
    __tablename__ = "submission_scores"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("evaluation_submissions.id"))
    criterion_id = Column(Integer, ForeignKey("criteria.id"))
    score = Column(Float, nullable=False)

    submission = relationship("EvaluationSubmission", back_populates="scores")
    criterion = relationship("Criterion", back_populates="submission_scores")
