from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ExtractedStructure(BaseModel):
    objective: str = Field(..., description="what is being optimized or solved")
    variables: List[str] = Field(..., description="list of key variables in the system")
    constraints: List[str] = Field(..., description="list of constraints the solution must satisfy")
    system_type: Literal["deterministic", "stochastic", "hybrid"] = Field(..., description="system type")
    equation_form: str = Field(..., description="description of the equation structure")
    optimization_type: Literal["min", "max", "equilibrium", "unknown"] = Field(..., description="optimization goal")
    problem_class: Literal["differential equation", "optimization", "inference", "simulation"] = Field(..., description="general category")
    domain_hint: Optional[str] = Field(None, description="what domain the user seems to be working in")
