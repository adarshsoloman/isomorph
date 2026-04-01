from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from .extraction import ExtractedStructure
from .primitive import PrimitiveInfo

class AnalogyMapping(BaseModel):
    variable_mapping: Dict[str, str] = Field(..., description="how researcher's variables map to this method")
    constraint_mapping: Dict[str, str] = Field(..., description="how researcher's constraints map")

class ScoredAnalogy(BaseModel):
    method_name: str = Field(..., description="canonical name of the matched method")
    origin_domain: str = Field(..., description="where this method comes from")
    appears_in: List[str] = Field(..., description="list of domains where it works")
    similarity_score: float = Field(..., description="0.0 – 1.0 similarity")
    mapping: AnalogyMapping
    transferable_aspects: List[str] = Field(..., description="what applies from this method")
    non_transferable_aspects: List[str] = Field(..., description="what does NOT transfer")
    failure_conditions: List[str] = Field(..., description="exactly where this analogy breaks down")
    primitive: Optional[PrimitiveInfo] = None

class AnalysisRequest(BaseModel):
    input_text: str = Field(..., description="raw text of the researcher's problem")

class AnalysisResponse(BaseModel):
    input_text: str
    extracted_structure: Optional[ExtractedStructure] = None
    analogies: List[ScoredAnalogy] = []
    confidence: float = 0.0
    errors: List[str] = []
    latency_ms: int = 0
    pipeline_version: str = "v0.1"
