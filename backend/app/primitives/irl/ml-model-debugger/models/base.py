from abc import ABC, abstractmethod
import numpy as np

class BaseModel(ABC):
    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the model on the provided dataset."""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate predictions for the given input features."""
        pass

    @abstractmethod
    def get_params(self) -> dict:
        """Return the current hyperparameter configuration."""
        pass

    @abstractmethod
    def set_params(self, params: dict):
        """Update the model's hyperparameters."""
        pass
