"""Tests for API routes."""

from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    """Test health check endpoint."""
    with patch("src.api.routes.health_agent") as mock_agent:
        mock_agent.get_health_status.return_value = {
            "timestamp": 12345.0,
            "system_health": {"test": {"healthy": True}},
        }

        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    with patch("src.api.routes.system_agent") as mock_agent:
        mock_agent.get_latest_metrics.return_value = {"cpu_percent": 50.0}

        response = client.get("/api/v1/metrics")
        assert response.status_code == 200
        assert "cpu_percent" in response.json()


def test_system_info_endpoint(client):
    """Test system info endpoint."""
    response = client.get("/api/v1/system/info")
    assert response.status_code == 200
    assert "platform" in response.json()
