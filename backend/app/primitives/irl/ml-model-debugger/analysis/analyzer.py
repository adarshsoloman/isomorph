from core.config import Config

class ModelDiagnosis:
    UNDERFITTING = "Underfitting"
    OVERFITTING = "Overfitting"
    ACCEPTABLE = "Acceptable"
    UNKNOWN = "Unknown"

class Analyzer:
    def __init__(self, min_threshold: float = None, high_threshold: float = None, overfitting_delta: float = None):
        """
        Initialize the analyzer with updated heuristics.
        """
        self.min_threshold = min_threshold or Config.MIN_ACCEPTABLE_THRESHOLD
        self.high_threshold = high_threshold or Config.HIGH_PERFORMANCE_THRESHOLD
        self.overfitting_delta = overfitting_delta or Config.OVERFITTING_SCORE_DELTA

    def diagnose(self, train_metrics: dict, val_metrics: dict) -> str:
        """
        Compare training and validation metrics to diagnose model behavior.
        """
        # Determine scores (R2 for regression, Accuracy for classification)
        train_score = train_metrics.get("r2") or train_metrics.get("accuracy") or 0
        val_score = val_metrics.get("r2") or val_metrics.get("accuracy") or 0

        # 1. Overfitting: Training score is significantly higher than validation score
        if (train_score - val_score) > self.overfitting_delta:
            return ModelDiagnosis.OVERFITTING

        # 2. Underfitting: Validation score is below the minimum floor
        if val_score < self.min_threshold:
            return ModelDiagnosis.UNDERFITTING

        # 3. Acceptable: Only if validation score is above high performance threshold
        if val_score >= self.high_threshold:
            return ModelDiagnosis.ACCEPTABLE

        # 4. Moderate: Default to underfitting to encourage refinement
        return ModelDiagnosis.UNDERFITTING
