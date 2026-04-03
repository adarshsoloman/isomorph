class Config:
    # Diagnostic Heuristics
    MIN_ACCEPTABLE_THRESHOLD = 0.70    # Below this is always Underfitting
    HIGH_PERFORMANCE_THRESHOLD = 0.85 # Above this is Truly Acceptable
    DEFAULT_OVERFITTING_RATIO = 1.15   # Val_Error / Train_Error (Legacy check)
    OVERFITTING_SCORE_DELTA = 0.15     # If Train_Score - Val_Score > this, it's Overfitting
    
    # Loop Settings
    MAX_ITERATIONS = 5
    IMPROVEMENT_THRESHOLD = 0.01      # Delta score required to continue
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
