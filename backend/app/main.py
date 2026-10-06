from fastapi import FastAPI

from app.routes.commissions.route import router as commissions_router


app = FastAPI(
    title="Business Operations Manager",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(commissions_router)