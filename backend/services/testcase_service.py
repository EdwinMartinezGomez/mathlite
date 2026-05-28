"""
Servicio mínimo para leer casos de prueba desde MongoDB.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://formales_db:formales1@cluster0.l18wsxl.mongodb.net/?appName=Cluster0")
MONGO_DB = os.getenv("MONGO_DB", "mathlite")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "test_cases")
SEED_FILE = Path(__file__).resolve().parents[1] / "data" / "test_cases_seed.json"


def _collection():
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI no está configurada")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    return client[MONGO_DB][MONGO_COLLECTION]


def _seed_if_empty(col) -> None:
    if col.count_documents({}) > 0:
        return
    if not SEED_FILE.exists():
        return

    with SEED_FILE.open("r", encoding="utf-8") as f:
        seed = json.load(f)

    if seed:
        col.insert_many(seed)


def list_tests() -> list[dict]:
    """Devuelve los casos de prueba almacenados en MongoDB."""
    try:
        col = _collection()
        _seed_if_empty(col)
        docs = list(col.find({}, {"_id": 0}).sort("id", 1))
        return docs
    except PyMongoError as exc:
        raise RuntimeError(f"no se pudo leer MongoDB: {exc}") from exc
