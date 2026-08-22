from fastapi import FastAPI


app = FastAPI(
    title="GigRoute Europe API",
    version="1.0.0",
)

# decorator
@app.get("/health")
def health_check():
    return {
        "status": "ok"
    } 