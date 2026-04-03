from typing import List, Dict, Any
from ..base import BasePrimitive

class IterativeRefinement(BasePrimitive):
    @property
    def name(self) -> str:
        return "Iterative Refinement"

    @property
    def description(self) -> str:
        return "Progressively improves a solution by reducing the error in each step."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "initial_guess": "number",
            "target": "number",
            "learning_rate": "number",
            "iterations": "integer"
        }

    @property
    def output_schema(self) -> Dict[str, Any]:
        return {
            "final_value": "number",
            "history": "list of numbers",
            "error": "number"
        }

    @property
    def assumptions(self) -> List[str]:
        return [
            "Objective function is continuous",
            "Gradient or direction of improvement can be estimated"
        ]

    @property
    def example_input(self) -> Dict[str, Any]:
        return {
            "initial_guess": 0.0,
            "target": 10.0,
            "learning_rate": 0.1,
            "iterations": 10
        }

    @property
    def expected_output(self) -> Dict[str, Any]:
        return {
            "final_value": 6.51,
            "history": [0.0, 1.0, 1.9, 2.71, 3.44, 4.09, 4.69, 5.22, 5.70, 6.13, 6.51],
            "error": 3.49
        }

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        A simple implementation of iterative refinement (gradient-descent-like).
        """
        current = float(input_data.get("initial_guess", 0.0))
        target = float(input_data.get("target", 1.0))
        lr = float(input_data.get("learning_rate", 0.1))
        iters = int(input_data.get("iterations", 10))
        
        history = [current]
        for _ in range(iters):
            # Move towards target
            current += (target - current) * lr
            history.append(round(current, 2))
            
        return {
            "final_value": round(current, 2),
            "history": history,
            "error": round(abs(target - current), 2)
        }
