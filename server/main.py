# server/main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from server.database import SessionLocal, init_db
from server import crud
from server.schemas import ClientRegister, ModelUpdate, AggregatedModel
from server.aggregation import aggregate_weights

# Initialize DB tables
init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="FedLearnOps Backend", version="0.2")


@app.post("/register")
def register_client(client: ClientRegister, db: Session = Depends(get_db)):
    success = crud.register_client(db, client.client_id, client.metadata)
    if not success:
        raise HTTPException(status_code=400, detail="Client already registered")
    return {"status": "registered", "client_id": client.client_id}


@app.post("/submit_update")
def submit_update(update: ModelUpdate, db: Session = Depends(get_db)):
    # Check client exists
    client_exists = crud.register_client(db, update.client_id, {})  # false if exists
    if client_exists:  # client did not exist before
        raise HTTPException(status_code=400, detail="Client not registered")
    
    # Save update
    crud.save_model_update(db, update.client_id, update.weights, update.metrics)
    return {"status": "received", "client_id": update.client_id}


@app.get("/aggregate", response_model=AggregatedModel)
def aggregate(db: Session = Depends(get_db)):
    updates = crud.get_all_model_updates(db)
    if not updates:
        raise HTTPException(status_code=400, detail="No updates to aggregate")
    
    weight_list = [u.weights for u in updates]
    aggregated_weights = aggregate_weights(weight_list)
    crud.clear_model_updates(db)
    return {"aggregated_weights": aggregated_weights.tolist()}


@app.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    updates = crud.get_all_model_updates(db)
    if not updates:
        return {"message": "No updates yet"}
    import numpy as np
    metrics_summary = {
        "num_clients": len(updates),
        "avg_accuracy": float(np.mean([u.metrics["accuracy"] for u in updates])),
        "avg_loss": float(np.mean([u.metrics["loss"] for u in updates]))
    }
    return metrics_summary