"""Main application entry point."""
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api.routes import health_agent, router, system_agent
from src.config.settings import settings
from src.utils.logger import logger

# Global task references
monitoring_tasks = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting monitoring system", version=settings.app_version)

    # Start monitoring agents
    monitoring_tasks.extend(
        [
            asyncio.create_task(system_agent.run()),
            asyncio.create_task(health_agent.run()),
        ]
    )

    logger.info("Monitoring agents started")

    yield

    # Shutdown
    logger.info("Shutting down monitoring system")

    # Stop monitoring agents
    system_agent.stop()
    health_agent.stop()

    # Cancel tasks
    for task in monitoring_tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    logger.info("Monitoring system stopped")


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Cloud Infrastructure Monitoring & Alerting System",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Add root redirect
    @app.get("/")
    async def root():
        """Redirect root to API docs."""
        return RedirectResponse(url="/docs")

    # Include routers
    app.include_router(router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
