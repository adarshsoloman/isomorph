from typing import Dict, Type, Optional
from .base import BasePrimitive
from .implementations.iterative_refinement import IterativeRefinement
from .implementations.ml_debugger_irl import MLModelDebuggerIRL

# Registry of method_name -> Primitive class
PRIMITIVE_REGISTRY: Dict[str, Type[BasePrimitive]] = {
    "Stochastic Gradient Descent (SGD)": MLModelDebuggerIRL,
    "Iterative Refinement": IterativeRefinement,
}

def get_primitive_for_method(method_name: str) -> Optional[BasePrimitive]:
    """
    Returns an instance of the primitive for a given method name.
    """
    primitive_class = PRIMITIVE_REGISTRY.get(method_name)
    if primitive_class:
        return primitive_class()
    return None
