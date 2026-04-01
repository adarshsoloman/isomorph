import uuid
from sqlalchemy import Column, String, Text, Boolean, JSON, ARRAY, UUID, Float, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from .base import Base

class Method(Base):
    __tablename__ = "methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    aliases = Column(ARRAY(String), default=[])
    origin_domain = Column(String(255), nullable=False)
    appears_in = Column(ARRAY(String), default=[])
    mathematical_core = Column(Text, nullable=False)
    problem_class = Column(String(255), nullable=False) # optimization / inference / simulation / classification
    equation_class = Column(String(255), nullable=False) # differential / algebraic / probabilistic / geometric
    constraint_type = Column(String(255), nullable=False) # physical laws / boundary conditions / conservation laws
    cross_domain_example_1 = Column(Text)
    cross_domain_example_2 = Column(Text)
    where_analogy_breaks = Column(Text, nullable=False)
    assumptions = Column(ARRAY(String), default=[])
    runnable = Column(Boolean, default=False)
    python_implementation = Column(String(255))
    tags = Column(ARRAY(String), default=[])
    embedding = Column(Vector(384)) # matches sentence-transformers all-MiniLM-L6-v2
    complexity_level = Column(String(50)) # basic / intermediate / advanced
    typical_use_cases = Column(ARRAY(String), default=[])
    known_limitations = Column(ARRAY(String), default=[])

    # Relationship to primitives
    primitives = relationship("Primitive", back_populates="method", cascade="all, delete-orphan")

class Primitive(Base):
    __tablename__ = "primitives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    method_id = Column(UUID(as_uuid=True), ForeignKey("methods.id", ondelete="CASCADE"), nullable=False)
    method_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    input_schema = Column(JSON, nullable=False)
    output_schema = Column(JSON, nullable=False)
    assumptions = Column(ARRAY(String), default=[])
    version = Column(String(50), default="1.0.0")
    active = Column(Boolean, default=True)

    # Link back to Method
    method = relationship("Method", back_populates="primitives")
