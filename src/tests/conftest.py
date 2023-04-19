from ..main import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="function")
def client():
    return TestClient(app)
