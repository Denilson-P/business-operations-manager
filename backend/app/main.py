from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.commissions.route import router as commissions_router
from app.routes.inventory.route import router as inventory_router
from app.routes.interest.route import router as interest_router



app = FastAPI(
    title="Business Operations Manager",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(commissions_router)
app.include_router(interest_router)
app.include_router(inventory_router)