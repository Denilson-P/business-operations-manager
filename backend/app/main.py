from fastapi import FastAPI

app = FastAPI(
    title="Business Operations Manager",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}