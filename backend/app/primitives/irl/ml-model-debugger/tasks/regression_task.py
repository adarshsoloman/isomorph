from tasks.base import BaseTask
from models.base import BaseModel
from evaluation.metrics import RegressionMetrics
import numpy as np

class RegressionTask(BaseTask):
    def evaluate(self, model: BaseModel, X: np.ndarray, y: np.ndarray) -> dict:
        predictions = model.predict(X)
        return RegressionMetrics.calculate(y, predictions)
