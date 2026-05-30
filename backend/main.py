"""
MathLite API — servidor FastAPI.

Expone los endpoints que consume el frontend:
- GET /api/health
- GET /api/tests
- POST /api/run
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.expression_routes import router as expression_router

app = FastAPI(title="MathLite API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expression_router)


@app.get("/")
def root():
    return "MathLite API"
