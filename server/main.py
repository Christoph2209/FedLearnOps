from fastapi import FastAPI
import numpy as np

app = FastAPI()

clients = {}
model_updates = []

@app.post("/register")
def register_client(client_id: str):
    clients[client_id] = {}
    return {"status": "registered"}

@app.post("/submit_update")
def submit_update(client_id: str, weights: list, metrics: dict):
    model_updates.append({"client_id": client_id, "weights": weights, "metrics": metrics})
    return {"status": "received"}

@app.get("/aggregate")
def aggregate():
    if not model_updates:
        return {"message": "No updates yet"}
    
    avg_weights = np.mean([np.array(u["weights"]) for u in model_updates], axis=0).tolist()
    model_updates.clear()
    return {"aggregated_weights": avg_weights}