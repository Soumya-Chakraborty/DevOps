"""Tests for monitoring agents."""

import asyncio
from unittest.mock import Mock, patch

import pytest

from src.monitoring.agents import HealthCheckAgent, SystemMonitoringAgent


@pytest.fixture
def system_agent():
    """Create a SystemMonitoringAgent instance."""
    return SystemMonitoringAgent()


@pytest.fixture
def health_agent():
    """Create a HealthCheckAgent instance."""
    return HealthCheckAgent()


class TestSystemMonitoringAgent:
    """Test SystemMonitoringAgent."""

    @pytest.mark.asyncio
    async def test_collect_data(self, system_agent):
        """Test data collection."""
        with patch.object(
            system_agent.system_collector, "collect_metrics"
        ) as mock_collect:
            mock_collect.return_value = Mock(timestamp=12345.0)
            with patch.object(
                system_agent.process_collector, "collect_top_processes"
            ) as mock_processes:
                mock_processes.return_value = []

                data = await system_agent.collect_data()

                assert "system_metrics" in data
                assert "top_processes" in data
                assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_process_data(self, system_agent):
        """Test data processing."""
        test_data = {
            "system_metrics": Mock(
                cpu_percent=50.0, memory_percent=60.0, disk_usage={}
            ),
            "timestamp": 12345.0,
        }

        await system_agent.process_data(test_data)
        assert len(system_agent.metrics_history) == 1

    def test_get_latest_metrics(self, system_agent):
        """Test getting latest metrics."""
        system_agent.metrics_history = [{"test": "data"}]
        latest = system_agent.get_latest_metrics()
        assert latest == {"test": "data"}


class TestHealthCheckAgent:
    """Test HealthCheckAgent."""

    @pytest.mark.asyncio
    async def test_collect_data(self, health_agent):
        """Test health check data collection."""
        data = await health_agent.collect_data()

        assert "system_health" in data
        assert "service_health" in data
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_process_data(self, health_agent):
        """Test health check data processing."""
        test_data = {
            "system_health": {"test_check": {"healthy": True}},
            "service_health": {},
            "timestamp": 12345.0,
        }

        await health_agent.process_data(test_data)
        assert health_agent.health_status == test_data
