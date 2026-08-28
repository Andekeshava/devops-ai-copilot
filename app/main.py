from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


from app.analysis_router import (
    router as analysis_router
)

from app.stats_router import (
    router as stats_router
)


from app.history_router import (
    router as history_router
)


from app.database import (
    Base,
    engine
)


app = FastAPI(
    title="DevOps AI Copilot"
)

app.include_router(
    analysis_router
)

app.include_router(
    history_router
)

app.include_router(
    stats_router
)


# Create SQLite database tables
Base.metadata.create_all(
    bind=engine
)


# Serve static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)



# Serve frontend
@app.get("/")
def home():

    return FileResponse(
        "static/index.html"
    )


# Health check
@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "devops-ai-copilot"
    }
