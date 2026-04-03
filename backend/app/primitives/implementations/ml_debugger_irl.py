import subprocess
import os
import json
import sys
from typing import List, Dict, Any
from ..base import BasePrimitive

class MLModelDebuggerIRL(BasePrimitive):
    @property
    def name(self) -> str:
        return "ML Model Debugger (IRL)"

    @property
    def description(self) -> str:
        return "Automated Iterative Refinement Loop (IRL) for diagnosing and fixing ML model performance."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "data_path": "string (optional, path to CSV)",
            "target": "string (optional, target column name)",
            "task": "string (regression | classification)",
            "model": "string (linear | tree | forest)",
            "iters": "integer (max iterations)"
        }

    @property
    def output_schema(self) -> Dict[str, Any]:
        return {
            "final_metrics": "dict",
            "history": "list of dicts",
            "status": "string"
        }

    @property
    def assumptions(self) -> List[str]:
        return [
            "Dataset is in CSV format",
            "Target column exists in the dataset",
            "Task type matches the target variable (continuous vs categorical)"
        ]

    @property
    def example_input(self) -> Dict[str, Any]:
        return {
            "task": "regression",
            "model": "linear",
            "iters": 3
        }

    @property
    def expected_output(self) -> Dict[str, Any]:
        return {
            "status": "completed",
            "final_metrics": {"rmse": 0.45},
            "history": []
        }

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the ML Model Debugger IRL via subprocess.
        """
        # Path to the debugger script
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        irl_path = os.path.join(base_path, "irl")
        script_path = os.path.join(irl_path, "ml-model-debugger", "main.py")
        
        # Use the virtual environment within the irl folder
        if sys.platform == "win32":
            python_exe = os.path.join(irl_path, ".venv", "Scripts", "python.exe")
        else:
            python_exe = os.path.join(irl_path, ".venv", "bin", "python")

        # Build command
        cmd = [
            python_exe,
            script_path,
            "--task", input_data.get("task", "regression"),
            "--model", input_data.get("model", "linear"),
            "--iters", str(input_data.get("iters", 5))
        ]

        if input_data.get("data_path"):
            cmd.extend(["--data", input_data["data_path"]])
        if input_data.get("target"):
            cmd.extend(["--target", input_data["target"]])

        try:
            # Run the debugger
            # Note: The current main.py prints to stdout, it doesn't return JSON.
            # In a real production system, we'd modify main.py to have a --json flag.
            # For now, we capture the output.
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=irl_path,
                check=True
            )
            
            return {
                "status": "completed",
                "raw_output": result.stdout,
                "msg": "IRL process executed successfully."
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "failed",
                "error": e.stderr or str(e),
                "stdout": e.stdout
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
