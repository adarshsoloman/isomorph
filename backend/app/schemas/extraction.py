from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class VariableRoles(BaseModel):
    state: List[str] = Field(default_factory=list, description="variables defining the system's state")
    control: List[str] = Field(default_factory=list, description="variables that can be manipulated")
    noise: List[str] = Field(default_factory=list, description="stochastic or unpredictable elements")
    parameters: List[str] = Field(default_factory=list, description="fixed constants in the system")

class ExtractedStructure(BaseModel):
    is_scientific: bool = Field(..., description="whether the input describes a valid scientific/engineering problem")
    structure_confidence: float = Field(..., description="confidence in the structural extraction (0.0 to 1.0)")
    rejection_reason: Optional[str] = Field(None, description="why the problem was rejected if is_scientific is false")
    
    objective: Optional[str] = Field(None, description="what is being optimized or solved")
    variable_roles: VariableRoles = Field(default_factory=VariableRoles)
    constraints: List[str] = Field(default_factory=list, description="list of constraints the solution must satisfy")
    system_type: Optional[Literal["deterministic", "stochastic", "hybrid"]] = Field(None, description="system type")
    equation_form: Optional[str] = Field(None, description="description of the equation structure (e.g., linear, non-linear, partial differential)")
    optimization_type: Optional[Literal["min", "max", "equilibrium", "unknown"]] = Field(None, description="optimization goal")
    problem_class: Optional[Literal["differential equation", "optimization", "inference", "simulation"]] = Field(None, description="general category")
    domain_hint: Optional[str] = Field(None, description="what domain the user seems to be working in")
