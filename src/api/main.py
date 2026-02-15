from fastapi import FastAPI
from tracelens.api.routes import router

app = FastAPI(
    title="TraceLens",
    version="1.0.0",
    description="Cloud-native observability analysis system"
)

app.include_router(router)
