import json
import os
import copy
from tqdm import tqdm
from data.loader import DataLoader
from analysis.analyzer import Analyzer, ModelDiagnosis
from suggestions.suggester import Suggester
from core.fix_engine import FixEngine
from tasks.base import BaseTask
from models.base import BaseModel
from core.config import Config

class IterativeLoop:
    def __init__(self, model: BaseModel, task: BaseTask, data_loader: DataLoader, 
                 max_iterations: int = Config.MAX_ITERATIONS, 
                 improvement_threshold: float = Config.IMPROVEMENT_THRESHOLD,
                 verbose: bool = True):
        self.model = model
        self.task = task
        self.data_loader = data_loader
        self.max_iterations = max_iterations
        self.improvement_threshold = improvement_threshold
        self.verbose = verbose
        
        self.analyzer = Analyzer()
        self.suggester = Suggester()
        
        self.results = []
        self.best_score = -float('inf')
        self.best_model = None
        self.best_model_name = ""
        
        # Action Memory: Stores (model_name, action_name)
        self.failed_actions = set()
        self.last_action = None

    def run(self):
        if self.verbose:
            print("\n" + "="*50)
            print("  STARTING ITERATIVE REFINEMENT LOOP (IRL)")
            print("="*50)
            
        X_train, X_test, y_train, y_test = self.data_loader.load_and_split()
        
        for i in range(1, self.max_iterations + 1):
            model_name = type(self.model).__name__
            
            if self.verbose:
                print(f"\n[ITERATION {i}] - Current Model: {model_name}")
                pbar = tqdm(total=4, desc="Progress", unit="step", leave=False)
            else:
                pbar = None

            # 1. Training
            if pbar: pbar.set_description("Training model")
            self.model.train(X_train, y_train)
            if pbar: pbar.update(1)
            
            # 2. Evaluation
            if pbar: pbar.set_description("Evaluating model")
            train_metrics = self.task.evaluate(self.model, X_train, y_train)
            val_metrics = self.task.evaluate(self.model, X_test, y_test)
            if pbar: pbar.update(1)
            
            current_score = val_metrics.get("r2") or val_metrics.get("accuracy") or 0
            
            # --- Best Model Protection & Failed Action Tracking ---
            is_rejected = False
            if current_score < self.best_score:
                if self.verbose:
                    print(f"\n>>> Rejected change: Score decreased from {round(self.best_score, 4)} to {round(current_score, 4)}.")
                    if self.last_action:
                        print(f">>> Recording failed action: ('{model_name}', '{self.last_action}')")
                        self.failed_actions.add((model_name, self.last_action))
                    print(f">>> Reverting to previous best model ({self.best_model_name}).")
                
                self.model = copy.deepcopy(self.best_model)
                is_rejected = True
                # Re-evaluate for consistent diagnosis
                train_metrics = self.task.evaluate(self.model, X_train, y_train)
                val_metrics = self.task.evaluate(self.model, X_test, y_test)
                current_score = self.best_score
                model_name = self.best_model_name
            else:
                self.best_score = current_score
                self.best_model = copy.deepcopy(self.model)
                self.best_model_name = model_name

            # 3. Diagnosis
            if pbar: pbar.set_description("Analyzing performance")
            diagnosis = self.analyzer.diagnose(train_metrics, val_metrics)
            if pbar: pbar.update(1)
            
            # 4. Suggestion
            if pbar: pbar.set_description("Generating suggestions")
            suggestion = self.suggester.suggest(diagnosis, model_name)
            if pbar: pbar.update(1)
            
            if pbar: pbar.close()

            action_to_apply = suggestion['action']
            
            # --- Check if action has already failed ---
            if (model_name, action_to_apply) in self.failed_actions:
                if self.verbose:
                    print(f">>> Skipping failed action '{action_to_apply}' for {model_name}.")
                
                # Attempt alternative via FixEngine (passing failed actions)
                alternative_model = FixEngine.get_alternative(self.model, action_to_apply, self.failed_actions)
                if alternative_model:
                    if self.verbose: print(">>> Found alternative strategy.")
                    self.model = alternative_model
                    self.last_action = f"Alternative for {action_to_apply}"
                else:
                    if self.verbose: print(">>> No effective actions remaining for this path.")
                    # If no alternative and we are not already at acceptable performance, stop loop
                    if diagnosis != ModelDiagnosis.ACCEPTABLE:
                        self._save_results()
                        self._print_final_summary()
                        return self.model
                    action_to_apply = "None (Exhausted)"
            else:
                # 5. Fix (Normal path)
                if diagnosis != ModelDiagnosis.ACCEPTABLE:
                    self.model = FixEngine.apply_fix(self.model, suggestion)
                    self.last_action = action_to_apply
                else:
                    self.last_action = "None"

            # Result Tracking
            iteration_result = {
                "iteration": i,
                "model": model_name,
                "score": round(current_score, 4),
                "diagnosis": diagnosis,
                "action": "Reverted (Skip Fix)" if is_rejected else action_to_apply,
                "metrics": val_metrics
            }
            self.results.append(iteration_result)

            if self.verbose:
                print(f"  Score:     {iteration_result['score']}")
                print(f"  Diagnosis: {diagnosis}")
                print(f"  Action:    {iteration_result['action']}")

            # --- STOP CONDITIONS ---
            if diagnosis == ModelDiagnosis.ACCEPTABLE:
                if self.verbose: print(f"\n>>> Stopping: Performance reached high threshold ({Config.HIGH_PERFORMANCE_THRESHOLD}).")
                break
            
            if i > 1 and not is_rejected:
                delta = current_score - self.results[-2]['score']
                if delta < self.improvement_threshold:
                    if self.verbose: print(f"\n>>> Stopping: Improvement plateaued (delta {round(delta, 4)} < {self.improvement_threshold}).")
                    break
                
            if i == self.max_iterations:
                if self.verbose: print("\n>>> Stopping: Maximum iterations reached.")
                break
            
        self._save_results()
        self._print_final_summary()
        return self.model

    def _save_results(self, filename="results.json"):
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, filename)
        with open(path, 'w') as f:
            json.dump(self.results, f, indent=4)
        if self.verbose:
            print(f"\nDetailed results saved to {path}")

    def _print_final_summary(self):
        print("\n" + "="*50)
        print("  FINAL SUMMARY")
        print("="*50)
        print(f"  Best Model: {self.best_model_name}")
        print(f"  Best Score: {round(self.best_score, 4)}")
        print("="*50 + "\n")
