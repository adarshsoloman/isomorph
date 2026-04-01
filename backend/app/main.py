from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes import analyze, health

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        docs_url="/docs"
    )

    # CORS configuration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, restrict to frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Routes
    application.include_router(analyze.router, prefix="/analyze", tags=["analysis"])
    application.include_router(health.router, prefix="/health", tags=["system"])

    return application

app = get_application()

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.PIPELINE_VERSION,
        "docs": "/docs"
    }
