from fastapi.testclient import TestClient
from main import app, classify_intent, clean_input, generate_response

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


def test_ai_endpoint_success():
    payload = {"question": "Tell me a joke"}
    response = client.post("/api/ai", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0


def test_ai_endpoint_empty_question():
    response = client.post("/api/ai", json={"question": ""})
    assert response.status_code == 200  # If it is empty it is not considered an error
    assert "answer" in response.json()


def test_ai_endpoint_invalid_payload():
    response = client.post("/api/ai", json={})
    assert response.status_code == 422  # Validation error because the "question" field was not sent


def test_ai_endpoint_trigger_error(monkeypatch):
    def mock_classify_intent(text):
        raise Exception("Mocked failure")

    # Patch classify_intent to raise errors
    monkeypatch.setattr("main.classify_intent", mock_classify_intent)

    response = client.post("/api/ai", json={"question": "Force error"})
    assert response.status_code == 500
    assert "error" in response.json()


def test_clean_input():
    assert clean_input(" Hello! ") == "hello"
    assert clean_input("What's this?") == "whats this"
    assert clean_input("   Clean   ME!! ") == "clean   me"


def test_classify_intent():
    assert classify_intent("hello") == "greeting"
    assert classify_intent("bye") == "farewell"
    assert classify_intent("can you help me?") == "help"
    assert classify_intent("how are you doing?") == "feeling"
    assert classify_intent("thanks a lot") == "thanks"
    assert classify_intent("random unrelated text") == "unknown"


def test_generate_response_known():
    assert "assist" in generate_response("greeting", "hello")
    assert "Goodbye" in generate_response("farewell", "bye")
    assert "help" in generate_response("help", "need help")
    assert "great" in generate_response("feeling", "how are you?")
    assert "welcome" in generate_response("thanks", "thanks")


def test_generate_response_unknown_weather():
    assert "weather" in generate_response("unknown", "What's the weather like?")


def test_generate_response_unknown_time():
    assert "currently" in generate_response("unknown", "what time is it")


def test_generate_response_unknown_default():
    assert "not sure" in generate_response("unknown", "xyz123")
