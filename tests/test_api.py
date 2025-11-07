from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_redirect():
    # When hitting "/", client will follow redirect automatically,
    # so final response should be the UI HTML
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers.get("content-type", "")


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_predict_endpoint():
    payload = {
        "loan_amnt": 15000,
        "term": "36 months",
        "int_rate": 12.5,
        "installment": 350,
        "grade": "B",
        "sub_grade": "B4",
        "home_ownership": "MORTGAGE",
        "annual_inc": 75000,
        "purpose": "credit_card",
        "dti": 18.2,
        "open_acc": 6,
        "revol_bal": 4500,
        "revol_util": 42.3,
        "tot_cur_bal": 25000,
        "fico_score": 710,
    }

    res = client.post("/predict", json=payload)
    assert res.status_code == 200

    data = res.json()
    assert "prediction" in data
    assert "default_probability" in data
