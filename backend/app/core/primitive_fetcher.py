from typing import Optional
from ..primitives.registry import get_primitive_for_method
from ..schemas.primitive import PrimitiveInfo

class PrimitiveFetcher:
    def fetch_for_method(self, method_name: str) -> Optional[PrimitiveInfo]:
        """
        Check if a runnable primitive exists for the given method.
        If it does, return the metadata.
        """
        primitive = get_primitive_for_method(method_name)
        if not primitive:
            return None

        return PrimitiveInfo(
            name=primitive.name,
            description=primitive.description,
            input_schema=primitive.input_schema,
            output_schema=primitive.output_schema,
            assumptions=primitive.assumptions,
            example_input=primitive.example_input,
            expected_output=primitive.expected_output
        )

# Singleton instance
primitive_fetcher = PrimitiveFetcher()
