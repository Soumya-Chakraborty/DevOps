"""API routes for the monitoring system."""
from fastapi import APIRouter, HTTPException

from src.monitoring.agents import HealthCheckAgent, SystemMonitoringAgent
from src.utils.logger import logger

# Global agent instances (in production, use dependency injection)
system_agent = SystemMonitoringAgent()
health_agent = HealthCheckAgent()

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Cloud Infrastructure Monitoring System", "version": "1.0.0"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        health_status = health_agent.get_health_status()
        return {
            "status": "healthy",
            "timestamp": health_status.get("timestamp"),
            "checks": health_status,
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/metrics")
async def get_metrics():
    """Get current system metrics."""
    try:
        metrics = system_agent.get_latest_metrics()
        if not metrics:
            raise HTTPException(status_code=404, detail="No metrics available")
        return metrics
    except Exception as e:
        logger.error("Failed to get metrics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")


@router.get("/metrics/history")
async def get_metrics_history(limit: int = 50):
    """Get historical metrics."""
    try:
        history = system_agent.get_metrics_history(limit)
        return {"count": len(history), "metrics": history}
    except Exception as e:
        logger.error("Failed to get metrics history", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to retrieve metrics history"
        )


@router.get("/system/info")
async def get_system_info():
    """Get basic system information."""
    try:
        import platform

        import psutil

        boot_time = psutil.boot_time()
        return {
            "platform": platform.platform(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "boot_time": boot_time,
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
        }
    except Exception as e:
        logger.error("Failed to get system info", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to retrieve system information"
        )
