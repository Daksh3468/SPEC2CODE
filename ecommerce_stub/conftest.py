"""
conftest.py — pytest fixtures for ecommerce_stub tests.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    """Return a FastAPI test client."""
    with TestClient(app) as c:
        yield c
