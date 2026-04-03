from analysis.analyzer import ModelDiagnosis

class Suggester:
    @staticmethod
    def suggest(diagnosis: str, current_model_type: str) -> dict:
        """
        Maps a diagnosis to a set of recommended actions.
        """
        if diagnosis == ModelDiagnosis.UNDERFITTING:
            return {
                "action": "Increase model complexity",
                "reason": "The model is too simple to capture the underlying patterns in the data.",
                "recommendation": "Try a Random Forest or increase the depth of the Decision Tree."
            }
        
        elif diagnosis == ModelDiagnosis.OVERFITTING:
            return {
                "action": "Apply regularization or reduce complexity",
                "reason": "The model has memorized the training data and is failing to generalize.",
                "recommendation": "Try Lasso/Ridge regression or decrease the maximum depth of the tree."
            }
        
        elif diagnosis == ModelDiagnosis.ACCEPTABLE:
            return {
                "action": "None",
                "reason": "The model performance is balanced and meets the stability criteria.",
                "recommendation": "The model is ready for deployment or further fine-tuning."
            }
        
        return {
            "action": "Review data",
            "reason": "The diagnosis is inconclusive.",
            "recommendation": "Check for data quality issues or feature-target correlation."
        }
