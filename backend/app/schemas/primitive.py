from pydantic import BaseModel
from typing import List, Dict, Any

class PrimitiveInfo(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    assumptions: List[str]
    version: str = "1.0.0"

class PrimitiveRunRequest(BaseModel):
    input_data: Dict[str, Any]

class PrimitiveRunResponse(BaseModel):
    output_data: Dict[str, Any]
    metadata: Dict[str, Any] = {}
