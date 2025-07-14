from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)

    alternatives = relationship("Alternative", back_populates="evaluation", cascade="all, delete-orphan")
    criteria = relationship("Criterion", back_populates="evaluation", cascade="all, delete-orphan")

class Alternative(Base):
    __tablename__ = "alternatives"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    proposer = Column(String)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=False)

    evaluation = relationship("Evaluation", back_populates="alternatives")
    notes = relationship("AlternativeCriterionNote", back_populates="alternative", cascade="all, delete-orphan")

class Criterion(Base):
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    weight = Column(Float, nullable=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=False)

    evaluation = relationship("Evaluation", back_populates="criteria")
    notes = relationship("AlternativeCriterionNote", back_populates="criterion", cascade="all, delete-orphan")

class AlternativeCriterionNote(Base):
    __tablename__ = "alternative_criterion_notes"
    __table_args__ = (UniqueConstraint('alternative_id', 'criterion_id', name='uq_alternative_criterion'),)

    id = Column(Integer, primary_key=True, index=True)
    alternative_id = Column(Integer, ForeignKey("alternatives.id"), nullable=False)
    criterion_id = Column(Integer, ForeignKey("criteria.id"), nullable=False)
    note = Column(Float, nullable=False)

    alternative = relationship("Alternative", back_populates="notes")
    criterion = relationship("Criterion", back_populates="notes")
