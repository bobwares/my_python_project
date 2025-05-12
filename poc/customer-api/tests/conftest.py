import pytest
from fastapi.testclient import TestClient
from customer_api.main import app

@pytest.fixture
def client():
    return TestClient(app)
