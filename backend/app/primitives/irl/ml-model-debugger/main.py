import argparse
import os
import sys
from data.loader import DataLoader
from models.regression import LinearRegressionModel, DecisionTreeModel, RandomForestModel
from models.classification import LogisticRegressionModel, DecisionTreeClassifierModel, RandomForestClassifierModel
from tasks.regression_task import RegressionTask
from tasks.classification_task import ClassificationTask
from core.loop import IterativeLoop
from core.config import Config

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_model(model_name: str, task_type: str):
    models = {
        "regression": {
            "linear": LinearRegressionModel,
            "tree": DecisionTreeModel,
            "forest": RandomForestModel
        },
        "classification": {
            "logistic": LogisticRegressionModel,
            "tree": DecisionTreeClassifierModel,
            "forest": RandomForestClassifierModel
        }
    }
    
    model_class = models.get(task_type, {}).get(model_name)
    if not model_class:
        raise ValueError(f"Model '{model_name}' not supported for task '{task_type}'")
    return model_class()

def main():
    parser = argparse.ArgumentParser(description="ML Model Debugger - Iterative Refinement Loop")
    
    parser.add_argument("--data", type=str, help="Path to the CSV dataset")
    parser.add_argument("--target", type=str, help="Name of the target column")
    parser.add_argument("--task", type=str, choices=["regression", "classification"], default="regression", help="Task type")
    parser.add_argument("--model", type=str, default="linear", help="Initial model (linear, logistic, tree, forest)")
    parser.add_argument("--iters", type=int, default=Config.MAX_ITERATIONS, help="Max iterations")
    parser.add_argument("--verbose", action="store_true", default=False, help="Show detailed logs for each iteration")

    args = parser.parse_args()

    # 1. Setup Data
    if not args.data or not args.target:
        if args.verbose:
            print(">>> No dataset provided. Running demo with sample_regression.csv...")
        data_path = "ml-model-debugger/data/sample_regression.csv"
        target_col = "target"
        if not os.path.exists(data_path):
            from utils.data_gen import generate_sample_data
            generate_sample_data(data_path)
    else:
        data_path = args.data
        target_col = args.target

    # 2. Initialize Components
    loader = DataLoader(file_path=data_path, target_column=target_col)
    
    # Map model name based on task
    model_key = "logistic" if args.task == "classification" and args.model == "linear" else args.model
    initial_model = get_model(model_key, args.task)
    
    task = RegressionTask() if args.task == "regression" else ClassificationTask()

    # 3. Run IRL
    debugger = IterativeLoop(
        model=initial_model,
        task=task,
        data_loader=loader,
        max_iterations=args.iters,
        verbose=args.verbose
    )

    debugger.run()

if __name__ == "__main__":
    main()
