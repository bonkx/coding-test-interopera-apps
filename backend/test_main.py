import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_sales_reps():
    response = client.get("/api/sales-reps")
    assert response.status_code == 200
    assert isinstance(response.json(), list) or isinstance(response.json(), dict)

    # check name in salesReps list
    assert "name" in response.json()["salesReps"][0]


def test_sales_reps_error_handling(mocker):
    # Simulasikan error saat load file dummy
    mocker.patch("main.load_dummy_data", side_effect=Exception("Simulated failure"))

    response = client.get("/api/sales-reps")
    assert response.status_code == 500
    assert "error" in response.json()
    assert "Simulated failure" in response.json()["error"]


def test_ai_endpoint_with_question():
    payload = {"question": "What is your name?"}
    response = client.post("/api/ai", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "What is your name?" in data["answer"]


def test_ai_endpoint_with_empty_question():
    payload = {}
    response = client.post("/api/ai", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "placeholder" in data["answer"]
