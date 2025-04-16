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


def test_deal_value_per_rep_success():
    response = client.get("/api/chart/deal-value-per-rep")
    assert response.status_code == 200

    data = response.json()
    assert "labels" in data
    assert "datasets" in data
    assert isinstance(data["labels"], list)
    assert isinstance(data["datasets"], list)
    assert len(data["datasets"]) == 1
    dataset = data["datasets"][0]

    assert "label" in dataset
    assert dataset["label"] == "Total Deal Value"
    assert "data" in dataset
    assert "backgroundColor" in dataset
    assert isinstance(dataset["data"], list)
    assert all(isinstance(value, (int, float)) for value in dataset["data"])


def test_deal_value_per_rep_failure(monkeypatch):
    # Simulasikan load_dummy_data raise Exception
    def mock_load_dummy_data():
        raise Exception("Simulated data loading error")

    monkeypatch.setattr("main.load_dummy_data", mock_load_dummy_data)

    response = client.get("/api/chart/deal-value-per-rep")
    assert response.status_code == 500
    assert response.json() == {"error": "Simulated data loading error"}


def test_top_clients_success():
    response = client.get("/api/chart/top-clients")
    assert response.status_code == 200

    data = response.json()
    assert "labels" in data
    assert "datasets" in data
    assert isinstance(data["labels"], list)
    assert isinstance(data["datasets"], list)

    dataset = data["datasets"][0]
    assert "label" in dataset
    assert "data" in dataset
    assert isinstance(dataset["data"], list)
    assert all(isinstance(value, (int, float)) for value in dataset["data"])


def test_top_clients_failure(monkeypatch):
    def mock_load_dummy_data():
        raise Exception("Simulated failure for top clients")

    monkeypatch.setattr("main.load_dummy_data", mock_load_dummy_data)

    response = client.get("/api/chart/top-clients")
    assert response.status_code == 500
    assert response.json() == {"error": "Simulated failure for top clients"}
