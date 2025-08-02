"""Monitoring agents for different system components."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.config.settings import settings
from src.monitoring.collectors import ProcessCollector, SystemCollector
from src.utils.logger import logger


class BaseAgent(ABC):
    """Base class for monitoring agents."""

    def __init__(self, name: str):
        self.name = name
        self.logger = logger.bind(agent=name)
        self.running = False

    @abstractmethod
    async def collect_data(self) -> Dict[str, Any]:
        """Collect monitoring data."""
        pass

    @abstractmethod
    async def process_data(self, data: Dict[str, Any]) -> None:
        """Process collected data."""
        pass

    async def run(self) -> None:
        """Main agent loop."""
        self.running = True
        self.logger.info(f"Starting {self.name} agent")

        while self.running:
            try:
                data = await self.collect_data()
                await self.process_data(data)
                await asyncio.sleep(settings.collection_interval)
            except Exception as e:
                self.logger.error(f"Error in {self.name} agent", error=str(e))
                await asyncio.sleep(5)

    def stop(self) -> None:
        """Stop the agent."""
        self.running = False
        self.logger.info(f"Stopping {self.name} agent")


class SystemMonitoringAgent(BaseAgent):
    """Agent for monitoring system metrics."""

    def __init__(self):
        super().__init__("SystemMonitoring")
        self.system_collector = SystemCollector()
        self.process_collector = ProcessCollector()
        self.metrics_history: List[Dict[str, Any]] = []

    async def collect_data(self) -> Dict[str, Any]:
        """Collect system and process data."""
        system_metrics = self.system_collector.collect_metrics()
        top_processes = self.process_collector.collect_top_processes()

        return {
            "system_metrics": system_metrics,
            "top_processes": top_processes,
            "timestamp": system_metrics.timestamp,
        }

    async def process_data(self, data: Dict[str, Any]) -> None:
        """Process and store collected data."""
        # Store in memory for now (Phase 1)
        self.metrics_history.append(data)

        # Keep only last 100 entries
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)

        # Check for alerts
        await self._check_alerts(data["system_metrics"])

    async def _check_alerts(self, metrics) -> None:
        """Check if any metrics exceed thresholds."""
        alerts = []

        if metrics.cpu_percent > settings.alert_threshold_cpu:
            alerts.append(f"High CPU usage: {metrics.cpu_percent:.1f}%")

        if metrics.memory_percent > settings.alert_threshold_memory:
            alerts.append(f"High memory usage: {metrics.memory_percent:.1f}%")

        for mount, usage in metrics.disk_usage.items():
            if usage["percent"] > settings.alert_threshold_disk:
                alerts.append(f"High disk usage on {mount}: {usage['percent']:.1f}%")

        if alerts:
            self.logger.warning("System alerts triggered", alerts=alerts)

    def get_latest_metrics(self) -> Dict[str, Any]:
        """Get the latest collected metrics."""
        return self.metrics_history[-1] if self.metrics_history else {}

    def get_metrics_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get historical metrics."""
        return self.metrics_history[-limit:]


class HealthCheckAgent(BaseAgent):
    """Agent for performing health checks."""

    def __init__(self):
        super().__init__("HealthCheck")
        self.health_status = {}

    async def collect_data(self) -> Dict[str, Any]:
        """Perform health checks."""
        checks = {
            "system_health": await self._check_system_health(),
            "service_health": await self._check_service_health(),
            "timestamp": asyncio.get_event_loop().time(),
        }
        return checks

    async def process_data(self, data: Dict[str, Any]) -> None:
        """Process health check results."""
        self.health_status = data

        # Log health status
        failed_checks = [
            check
            for check, status in data["system_health"].items()
            if not status["healthy"]
        ]

        if failed_checks:
            self.logger.warning("Health checks failed", failed_checks=failed_checks)
        else:
            self.logger.info("All health checks passed")

    async def _check_system_health(self) -> Dict[str, Any]:
        """Check system health indicators."""
        return {
            "disk_space": {
                "healthy": all(
                    usage["percent"] < 95
                    for usage in SystemCollector().collect_metrics().disk_usage.values()
                ),
                "description": "Disk space availability",
            },
            "memory": {
                "healthy": SystemCollector().collect_metrics().memory_percent < 95,
                "description": "Memory availability",
            },
        }

    async def _check_service_health(self) -> Dict[str, Any]:
        """Check service health (placeholder for Phase 1)."""
        return {
            "monitoring_service": {
                "healthy": True,
                "description": "Monitoring service status",
            }
        }

    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status."""
        return self.health_status
