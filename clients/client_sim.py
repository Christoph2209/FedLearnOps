# clients/client_sim.py

import requests
import numpy as np
import time

# -----------------------------
# Configuration
# -----------------------------
SERVER_URL = "http://127.0.0.1:8000"
NUM_CLIENTS = 3
WEIGHT_SIZE = 10        # Size of dummy model weights
ROUNDS = 2              # Number of federated rounds
SLEEP_TIME = 1          # Delay between updates (seconds)


# -----------------------------
# Helper functions
# -----------------------------
def register_client(client_id):
    response = requests.post(
        f"{SERVER_URL}/register",
        json={"client_id": client_id, "metadata": {"role": "simulated"}}
    )
    print(f"[{client_id}] Register response:", response.json())


def send_update(client_id):
    # Create dummy model weights and metrics
    weights = np.random.rand(WEIGHT_SIZE).tolist()
    metrics = {
        "accuracy": float(np.random.uniform(0.7, 1.0)),
        "loss": float(np.random.uniform(0.0, 0.5))
    }
    
    response = requests.post(
        f"{SERVER_URL}/submit_update",
        json={"client_id": client_id, "weights": weights, "metrics": metrics}
    )
    print(f"[{client_id}] Update response:", response.json())


# -----------------------------
# Main simulation
# -----------------------------
if __name__ == "__main__":
    # Step 1: Register clients
    client_ids = [f"client{i+1}" for i in range(NUM_CLIENTS)]
    for cid in client_ids:
        register_client(cid)
    
    # Step 2: Run federated rounds
    for r in range(ROUNDS):
        print(f"\n=== Federated Round {r+1} ===")
        for cid in client_ids:
            send_update(cid)
        
        # Optional: trigger aggregation
        response = requests.get(f"{SERVER_URL}/aggregate")
        print("Aggregated weights:", response.json()["aggregated_weights"])
        
        # Wait a bit before next round
        time.sleep(SLEEP_TIME)