# ML Model Debugger: Iterative Refinement Loop (IRL)

## 1. Executive Summary
The ML Model Debugger is a systematic framework designed to automate the lifecycle of machine learning model optimization. Unlike traditional AutoML platforms that focus on exhaustive search, this system implements an Iterative Refinement Loop (IRL) to diagnose performance bottlenecks and apply targeted architectural or hyperparameter corrections.

The goal is to move from stochastic experimentation to a deterministic, explainable refinement process.

---

## 2. The Iterative Refinement Loop (IRL)
The core of the system is a closed-loop control system that treats model training as a process to be monitored and corrected.

### System Flow Diagram
```text
    +-----------------------------------------------------------+
    |                  Iterative Refinement Loop                |
    |                                                           |
    |    +----------+         +------------+       +--------+   |
    |    |  TRAIN   | ------> |  EVALUATE  | ----> | OUTPUT |   |
    |    +----------+         +------------+       +--------+   |
    |          ^                    |                           |
    |          |                    V                           |
    |    +----------+         +------------+                    |
    |    |   FIX    | <------ |  DIAGNOSE  |                    |
    |    +----------+         +------------+                    |
    |          ^                    |                           |
    |          |                    V                           |
    |          +---------- [ SUGGESTIONS ] <--------------------+
    +-----------------------------------------------------------+
```

### Logical Stages
1. **Train**: Fitting the selected estimator on the training partition.
2. **Evaluate**: Extracting performance metrics (MSE/RMSE for Regression; Accuracy/F1 for Classification).
3. **Diagnose**: Analyzing the delta between training and validation error to identify Underfitting or Overfitting.
4. **Suggest**: Mapping the diagnosis to a specific correction policy (e.g., increasing complexity or applying regularization).
5. **Fix**: Programmatically updating the model configuration for the next iteration.

---

## 3. System Architecture
The codebase is strictly modular, adhering to the principle of separation of concerns.

```text
ml-model-debugger/
├── pyproject.toml      # Dependency management via uv
├── main.py             # System entry point
├── core/               # Loop orchestration and state management
├── models/             # Encapsulated model interfaces (Scikit-learn wrappers)
├── tasks/              # Task-specific logic (Regression vs. Classification)
├── evaluation/         # Metric calculation engine
├── analysis/           # Heuristic-based diagnostic engine
├── suggestions/        # Policy mapping (Diagnosis -> Action)
├── data/               # Ingestion and preprocessing pipelines
└── utils/              # Shared helper functions
```

---

## 4. Technical Stack
- **Runtime**: Python 3.10+
- **Environment Management**: uv (Fast, reliable dependency resolution)
- **Data Manipulation**: Pandas, NumPy
- **Estimators**: Scikit-learn (Linear Regression, Random Forest, etc.)

---

## 5. Installation and Setup
This project utilizes `uv` for environment management to ensure reproducible builds and low-latency dependency installation.

### Prerequisites
Ensure `uv` is installed on your system:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Environment Initialization
```bash
# Clone the repository
git clone <repository-url>
cd ml-model-debugger

# Create virtual environment and sync dependencies
uv sync
```

---

## 6. Usage
The system is controlled via a CLI interface. You can run the default demo or provide your own dataset and configuration.

### 6.1 Running the Demo
```bash
uv run ml-model-debugger/main.py
```

### 6.2 Running with Custom Configuration
```bash
uv run ml-model-debugger/main.py --data <path_to_csv> --target <target_column> --task <regression|classification> --model <linear|tree|forest> --iters <max_iterations>
```

#### CLI Arguments:
- `--data`: Path to the CSV dataset.
- `--target`: Name of the target (label) column.
- `--task`: Type of ML task (`regression` or `classification`).
- `--model`: Initial model architecture (`linear`, `tree`, `forest`).
- `--iters`: Maximum number of iterations for the refinement loop.

---

## 7. Design Principles

### 6.1 Modularity
Each component (Analyzer, Suggester, Fixer) operates as an independent unit. This allows for swapping the diagnostic logic without modifying the training loop.

### 6.2 Determinism
The system avoids "black-box" decision-making. Every suggestion made by the engine is logged with the corresponding diagnostic evidence, ensuring full auditability of the model's evolution.

### 6.3 Interface-Driven Development
Models are wrapped in a standard interface (`train`, `predict`), allowing the system to be agnostic of the underlying estimator's library.

---

## 7. Success Criteria
A successful execution is defined by:
- Convergence: The performance metric stabilizes or reaches a predefined threshold.
- Diagnostic Clarity: The system provides a clear log of why each change was made.
- Generalization: The final model performs consistently across cross-validation folds.

---

## 9. Roadmap
- [x] **Phase 1**: Core IRL implementation with tabular regression support.
- [x] **Phase 2**: Integration of classification tasks and complex heuristics.
- [ ] **Phase 3**: Automated feature engineering suggestions.
- [ ] **Phase 4**: Streamlit-based visualization dashboard.
