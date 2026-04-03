from abc import ABC, abstractmethod
from models.base import BaseModel
import numpy as np

class BaseTask(ABC):
    @abstractmethod
    def evaluate(self, model: BaseModel, X: np.ndarray, y: np.ndarray) -> dict:
        """Evaluate the model and return a dictionary of performance metrics."""
        pass
