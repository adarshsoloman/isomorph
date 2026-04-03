from fastapi import APIRouter
from typing import List
from ...primitives.registry import PRIMITIVE_REGISTRY
from ...schemas.primitive import PrimitiveInfo

router = APIRouter()

@router.get("/", response_model=List[PrimitiveInfo])
async def list_primitives():
    """
    List all available runnable primitives in the ISOMORPH system.
    """
    primitives = []
    for name, primitive_class in PRIMITIVE_REGISTRY.items():
        instance = primitive_class()
        primitives.append(PrimitiveInfo(
            name=instance.name,
            description=instance.description,
            input_schema=instance.input_schema,
            output_schema=instance.output_schema,
            assumptions=instance.assumptions,
            example_input=instance.example_input,
            expected_output=instance.expected_output
        ))
    return primitives
