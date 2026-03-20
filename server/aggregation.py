# server/aggregation.py

import numpy as np
from typing import List

# -----------------------------
# Simple aggregation: average
# -----------------------------
def aggregate_weights(weight_list: List[np.ndarray]) -> np.ndarray:
    """
    Aggregates a list of numpy arrays (model weights) by averaging them.
    
    Args:
        weight_list: List of np.ndarray, each representing a client's model weights
    
    Returns:
        np.ndarray: Averaged weights
    """
    if not weight_list:
        raise ValueError("No weights to aggregate")
    
    return np.mean(weight_list, axis=0)