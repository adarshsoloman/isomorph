from models.regression import LinearRegressionModel, RandomForestModel, DecisionTreeModel
from models.classification import LogisticRegressionModel, RandomForestClassifierModel, DecisionTreeClassifierModel
from models.base import BaseModel

class FixEngine:
    @staticmethod
    def apply_fix(current_model: BaseModel, suggestion: dict) -> BaseModel:
        """
        Applies improvements: Model switching or Hyperparameter adjustments.
        """
        action = suggestion.get("action")
        return FixEngine._execute_strategy(current_model, action)

    @staticmethod
    def get_alternative(current_model: BaseModel, failed_action: str, failed_actions: set) -> BaseModel:
        """
        Finds an alternative strategy if the primary action failed.
        """
        model_name = type(current_model).__name__
        
        if failed_action == "Increase model complexity":
            # If Switching to Random Forest failed, try Decision Tree
            if (model_name, "Switch to Decision Tree") not in failed_actions:
                if isinstance(current_model, (LinearRegressionModel, LogisticRegressionModel)):
                    print(">>> Alt Fix: Trying Decision Tree as alternative complexity boost.")
                    if isinstance(current_model, LinearRegressionModel):
                        return DecisionTreeModel(max_depth=10)
                    else:
                        return DecisionTreeClassifierModel(max_depth=10)
        
        elif failed_action == "Apply regularization or reduce complexity":
            # If reducing depth failed, maybe try a different model type or stricter pruning
            pass

        return None

    @staticmethod
    def _execute_strategy(current_model: BaseModel, action: str) -> BaseModel:
        if action == "Increase model complexity":
            if isinstance(current_model, (LinearRegressionModel, LogisticRegressionModel)):
                print(">>> Fix: Switching to Random Forest for more complexity.")
                if isinstance(current_model, LinearRegressionModel):
                    return RandomForestModel(n_estimators=100, random_state=42)
                else:
                    return RandomForestClassifierModel(n_estimators=100, random_state=42)
            
            if isinstance(current_model, (DecisionTreeModel, DecisionTreeClassifierModel)):
                print(">>> Fix: Increasing Tree complexity (max_depth=20).")
                current_model.set_params({"max_depth": 20})
                return current_model
        
        elif action == "Apply regularization or reduce complexity":
            print(">>> Fix: Applying regularization/reducing depth.")
            current_model.set_params({"max_depth": 5})
            return current_model
                
        return current_model
