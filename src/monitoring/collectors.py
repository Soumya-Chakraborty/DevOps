"""Data collectors for system metrics."""

import time
from dataclasses import dataclass
from typing import Any, Dict, List

import psutil

from src.utils.logger import logger


@dataclass
class SystemMetrics:
    """System metrics data structure."""

    timestamp: float
    cpu_percent: float
    memory_percent: float
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    process_count: int
    load_average: List[float]


class SystemCollector:
    """Collects system-level metrics."""

    def __init__(self):
        self.logger = logger.bind(component="SystemCollector")

    def collect_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Disk metrics
            disk_usage = {}
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = {
                        "total": partition_usage.total,
                        "used": partition_usage.used,
                        "free": partition_usage.free,
                        "percent": (partition_usage.used / partition_usage.total) * 100,
                    }
                except PermissionError:
                    continue

            # Network metrics
            network_io = psutil.net_io_counters()._asdict()

            # Process count
            process_count = len(psutil.pids())

            # Load average (Unix-like systems)
            try:
                load_average = list(psutil.getloadavg())
            except (AttributeError, OSError):
                load_average = [0.0, 0.0, 0.0]

            metrics = SystemMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage=disk_usage,
                network_io=network_io,
                process_count=process_count,
                load_average=load_average,
            )

            self.logger.info(
                "System metrics collected",
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                process_count=process_count,
            )

            return metrics

        except Exception as e:
            self.logger.error("Failed to collect system metrics", error=str(e))
            raise


class ProcessCollector:
    """Collects process-level metrics."""

    def __init__(self):
        self.logger = logger.bind(component="ProcessCollector")

    def collect_top_processes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Collect top processes by CPU usage."""
        try:
            processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent"]
            ):
                try:
                    proc_info = proc.info
                    proc_info["cpu_percent"] = proc.cpu_percent()
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by CPU usage and return top processes
            top_processes = sorted(
                processes, key=lambda x: x["cpu_percent"], reverse=True
            )[:limit]

            self.logger.info(f"Collected top {len(top_processes)} processes")
            return top_processes

        except Exception as e:
            self.logger.error("Failed to collect process metrics", error=str(e))
            raise
