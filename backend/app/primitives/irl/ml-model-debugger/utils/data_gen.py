import numpy as np
import pandas as pd
import os

def generate_sample_data(file_path: str):
    """
    Generates a simple non-linear dataset: y = x^2 + noise
    Linear regression should struggle with this, triggering the 'Fix' engine.
    """
    np.random.seed(42)
    X = np.random.rand(200, 3) * 10
    # y is non-linear relative to features
    y = (X[:, 0]**2) + (X[:, 1] * 2) + np.random.randn(200) * 2
    
    df = pd.DataFrame(X, columns=['feature_1', 'feature_2', 'feature_3'])
    df['target'] = y
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"Sample dataset created at: {file_path}")

if __name__ == "__main__":
    generate_sample_data("ml-model-debugger/data/sample_regression.csv")
