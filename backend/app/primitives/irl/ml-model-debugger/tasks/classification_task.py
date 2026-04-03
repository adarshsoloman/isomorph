from tasks.base import BaseTask
from models.base import BaseModel
from sklearn.metrics import accuracy_score
import numpy as np

class ClassificationTask(BaseTask):
    def evaluate(self, model: BaseModel, X: np.ndarray, y: np.ndarray) -> dict:
        predictions = model.predict(X)
        acc = accuracy_score(y, predictions)
        return {
            "accuracy": float(acc),
            "score": float(acc) # Generic score for analyzer
        }
