import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_root_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "operational"
    assert "BIS AI Copilot" in data["service"]

def test_health_endpoint(client):
    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    h_data = health_res.json()
    assert h_data["database"] == "healthy"
    assert "ai_engine" in h_data

def test_standards_search_and_exact_lookup(client):
    # 1. Broad search
    res = client.get("/api/standards?q=water heater")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] > 0
    assert any("302" in s["is_number"] for s in data["items"])

    # 2. Normalized IS lookup ("is 302", "IS302", "302")
    res_norm = client.get("/api/standards/lookup/IS 302 (Part 1)")
    assert res_norm.status_code == 200
    norm_data = res_norm.json()
    assert "302" in norm_data["is_number"]
    assert "Electrotechnical" in norm_data["division"]
    assert len(norm_data["applicable_qcos"]) > 0

    # 3. Filter by division
    res_div = client.get("/api/standards?division=ETD")
    assert res_div.status_code == 200
    assert res_div.json()["total"] > 0

    # 4. Filter by has_qco
    res_qco = client.get("/api/standards?has_qco=true")
    assert res_qco.status_code == 200
    assert res_qco.json()["total"] > 0

def test_qco_search_and_details(client):
    res = client.get("/api/qco?q=Toys")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] > 0
    toy_qco = data["items"][0]
    assert "Toys" in toy_qco["title"]
    assert "DPIIT" in toy_qco["issuing_ministry"]

    # Detail
    qco_id = toy_qco["id"]
    res_detail = client.get(f"/api/qco/{qco_id}")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert len(detail["standards"]) > 0
    assert len(detail["amendments"]) > 0

def test_laboratories_directory(client):
    # 1. State search
    res = client.get("/api/laboratories?state=Maharashtra")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] > 0
    assert any("Mumbai" in lab["city"] for lab in data["items"])

    # 2. Standard filter
    res_std = client.get("/api/laboratories?standard_is=IS 16046")
    assert res_std.status_code == 200
    data_std = res_std.json()
    assert data_std["total"] > 0

    # 3. Geo-distance calculation (e.g. coordinates near Delhi)
    res_geo = client.get("/api/laboratories?user_lat=28.6139&user_lon=77.2090")
    assert res_geo.status_code == 200
    data_geo = res_geo.json()
    assert data_geo["total"] > 0
    first_lab = data_geo["items"][0]
    assert first_lab["distance_km"] is not None

def test_checklist_crud_and_csv_export(client):
    # 1. Create
    payload = {
        "title": "Solar Inverter Certification",
        "product_name": "Grid Tie Solar Inverter",
        "standard_number": "IS 16221",
        "scheme_code": "SCHEME_II",
        "notes": "Testing checklist for production line 1",
        "tasks": [
            {
                "title": "Review Safety Guidelines",
                "stage": "Documentation",
                "is_mandatory": True,
                "order_index": 0
            }
        ]
    }
    create_res = client.post("/api/checklists", json=payload)
    assert create_res.status_code == 200
    c_data = create_res.json()
    c_id = c_data["id"]
    assert c_data["title"] == payload["title"]
    assert len(c_data["tasks"]) == 1

    # 2. Add task
    task_payload = {
        "title": "Schedule Lab Type Test",
        "stage": "Pre-Testing",
        "is_mandatory": True,
        "order_index": 1
    }
    add_res = client.post(f"/api/checklists/{c_id}/tasks", json=task_payload)
    assert add_res.status_code == 200
    updated_data = add_res.json()
    assert len(updated_data["tasks"]) == 2
    task_id = updated_data["tasks"][1]["id"]

    # 3. Mark task complete
    patch_res = client.patch(f"/api/checklists/{c_id}/tasks/{task_id}", json={"is_completed": True})
    assert patch_res.status_code == 200
    patch_data = patch_res.json()
    assert patch_data["completed_tasks"] == 1
    assert patch_data["completion_percentage"] == 50.0

    # 4. Export CSV
    csv_res = client.get(f"/api/checklists/{c_id}/export/csv")
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers["content-type"]
    assert "Grid Tie Solar Inverter" in csv_res.text
    assert "Schedule Lab Type Test" in csv_res.text

    # 5. Delete
    del_res = client.delete(f"/api/checklists/{c_id}")
    assert del_res.status_code == 200

    # Verify 404 after deletion
    get_res = client.get(f"/api/checklists/{c_id}")
    assert get_res.status_code == 404

def test_ai_navigator_workflow(client):
    payload = {
        "product_name": "Electric Storage Water Heater",
        "category": "Household Electrical",
        "intended_use": "Domestic bath water heating"
    }
    res = client.post("/api/ai/navigator", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["potentially_relevant_standards"]) > 0
    assert len(data["mandatory_qco_findings"]) > 0
    assert len(data["verified_facts"]) > 0
    assert len(data["citations"]) > 0
    assert data["certification_scheme"]["code"] == "SCHEME_I"

def test_coverage_dashboard(client):
    res = client.get("/api/stats/coverage")
    assert res.status_code == 200
    data = res.json()
    assert data["stats"]["total_standards"] >= 19
    assert data["stats"]["verified_standards"] >= 19
    assert data["stats"]["fixture_standards"] == 0
    assert data["stats"]["total_qcos"] >= 6
    assert data["stats"]["total_laboratories"] >= 10
    assert len(data["coverage_gaps"]) >= 3

def test_ai_chat_pipeline(client):
    # Test conversational RAG query
    payload = {
        "message": "I manufacture electric room heaters and electric irons. What standards apply, are there mandatory QCOs, and which labs can test them?"
    }
    res = client.post("/api/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["conversation_id"] is not None
    assert len(data["citations"]) > 0
    assert any("302" in c["identifier"] for c in data["citations"])
    assert len(data["identified_standards"]) > 0
    assert "Compliance Intelligence & Research Summary" in data["response"]
    assert "IS 302" in data["response"]
    assert data["latency_ms"] >= 0

    # Follow-up turn in same conversation
    conv_id = data["conversation_id"]
    payload2 = {
        "conversation_id": conv_id,
        "message": "Can I obtain Scheme-I certification without in-house test equipment?"
    }
    res2 = client.post("/api/ai/chat", json=payload2)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["conversation_id"] == conv_id
