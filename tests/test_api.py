import pytest
from starlette.testclient import TestClient
from api.main import app  # Import the app from api/main.py

@pytest.fixture
def client():
    """
    Create a TestClient instance that correctly handles the lifespan events.
    
    Using the 'with' statement is crucial as it triggers the
    startup (lifespan) event where our model is loaded.
    """
    with TestClient(app) as test_client:
        yield test_client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_positive(client):
    """Test the prediction endpoint with positive text."""
    payload = {"text": "i'm so happy and this is a great product"}
    response = client.post("/predict", json=payload)
    
    # We are debugging this assertion.
    # The 'with TestClient' in the fixture should now trigger the lifespan,
    # and we should see our print() logs.
    assert response.status_code == 200
    
    # Add more assertions to be robust
    data = response.json()
    assert data["text"] == payload["text"]
    assert "sentiment" in data