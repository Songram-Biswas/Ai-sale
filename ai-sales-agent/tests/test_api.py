from fastapi.testclient import TestClient

from app.main import app


def test_health():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analyze_company_stub():
    client = TestClient(app)
    r = client.post("/analyze_company", json={"company_url": "https://example.com"})
    assert r.status_code == 200
    body = r.json()
    assert "company" in body
    assert "insights" in body
    assert "sales_insights" in body["insights"]


def test_generate_report_both():
    client = TestClient(app)
    r = client.post(
        "/generate_report",
        json={
            "company": {"name": "ExampleCo", "url": "https://example.com"},
            "insights": {"sales_insights": ["a"], "pain_points": ["b"], "hooks": ["c"]},
            "format": "both",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "json" in body
    assert "markdown" in body

