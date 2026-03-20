# server/schemas.py

from pydantic import BaseModel
from typing import List, Dict, Optional

# -----------------------------
# Client registration schema
# -----------------------------
class ClientRegister(BaseModel):
    client_id: str
    metadata: Optional[Dict] = {}


# -----------------------------
# Model update schema
# -----------------------------
class ModelUpdate(BaseModel):
    client_id: str
    weights: List[float]      # List of model weights
    metrics: Dict[str, float] # Example: {"accuracy": 0.85, "loss": 0.3}


# -----------------------------
# Aggregated model response
# -----------------------------
class AggregatedModel(BaseModel):
    aggregated_weights: List[float]