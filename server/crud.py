# server/crud.py

from sqlalchemy.orm import Session
from server import database

# -----------------------------
# Clients
# -----------------------------
def register_client(db: Session, client_id: str, metadata: dict):
    from server.database import Client
    existing = db.query(Client).filter(Client.client_id == client_id).first()
    if existing:
        return False
    client = Client(client_id=client_id, client_metadata=metadata)
    db.add(client)
    db.commit()
    return True


# -----------------------------
# Model updates
# -----------------------------
def save_model_update(db: Session, client_id: str, weights: list, metrics: dict):
    from server.database import ModelUpdate
    update = ModelUpdate(client_id=client_id, weights=weights, metrics=metrics)
    db.add(update)
    db.commit()


def get_all_model_updates(db: Session):
    from server.database import ModelUpdate
    return db.query(ModelUpdate).all()


def clear_model_updates(db: Session):
    from server.database import ModelUpdate
    db.query(ModelUpdate).delete()
    db.commit()