import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

class RegressionMetrics:
    @staticmethod
    def calculate(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        """Calculate standard regression metrics."""
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        
        return {
            "mse": float(mse),
            "rmse": float(rmse),
            "r2": float(r2)
        }
