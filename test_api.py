from fastapi.testclient import TestClient
import pytest
from proiect_mainapi import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    yield
    # 1. Sterge dependentele mai intai (FK)
    client.delete("/Relationships/88823141/88823147")
    client.delete("/Relationships/88823147/88823148")
    client.delete("/Characteristics/CM-10001/Volume Test")
    client.delete("/Characteristics/CM-99001/Greutate")
    client.delete("/Characteristics/CM-99002/Culoare")
    # 2. Abia apoi tabelele de baza
    client.delete("/Identifiers/88823147")
    client.delete("/Identifiers/88823148")
    client.delete("/Countries/Austria")


# ── Identifiers ────────────────────────────────────────────────────────────────

def test_create_identifier():
    response = client.post("/Identifiers/", json={
        "identifier_name": "88823147",
        "description": "Conditioner Bottle",
        "identifier_type": "Finished Product Part"
    })
    assert response.status_code == 200
    assert response.json()["identifier_name"] == "88823147"

def test_get_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "88823147",
        "description": "Conditioner Bottle",
        "identifier_type": "Finished Product Part"
    })
    response = client.get("/Identifiers/88823147")
    assert response.status_code == 200
    assert response.json()["identifier_name"] == "88823147"

def test_get_identifier_not_found():
    response = client.get("/Identifiers/99999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Identifier not found"}

def test_put_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "88823147",
        "description": "Conditioner Bottle",
        "identifier_type": "Finished Product Part"
    })
    response = client.put("/Identifiers/88823147", json={
        "identifier_name": "88823147",
        "description": "Conditioner Bottle 500ml",
        "identifier_type": "Finished Product Part"
    })
    assert response.status_code == 200
    assert response.json()["description"] == "Conditioner Bottle 500ml"

def test_patch_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "88823147",
        "description": "Conditioner Bottle",
        "identifier_type": "Finished Product Part"
    })
    response = client.patch("/Identifiers/88823147", json={"identifier_type": "Packaging Material Part"})
    assert response.status_code == 200
    assert response.json()["identifier_type"] == "Packaging Material Part"

def test_delete_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "88823147",
        "description": "Conditioner Bottle",
        "identifier_type": "Finished Product Part"
    })
    response = client.delete("/Identifiers/88823147")
    assert response.status_code == 200
    assert response.json() == {"detail": "Identifier '88823147' deleted"}
    assert client.get("/Identifiers/88823147").status_code == 404


# ── Countries ──────────────────────────────────────────────────────────────────

def test_create_country():
    response = client.post("/Countries/", json={
        "name": "Austria",
        "iso_code": "AT",
        "short_code": 40
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Austria"

def test_get_country():
    client.post("/Countries/", json={
        "name": "Austria",
        "iso_code": "AT",
        "short_code": 40
    })
    response = client.get("/Countries/Austria")
    assert response.status_code == 200
    assert response.json()["name"] == "Austria"

def test_get_country_not_found():
    response = client.get("/Countries/Narnia")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}

def test_put_country():
    client.post("/Countries/", json={
        "name": "Austria",
        "iso_code": "AT",
        "short_code": 40
    })
    response = client.put("/Countries/Austria", json={
        "name": "Austria",
        "iso_code": "AUT",
        "short_code": 40
    })
    assert response.status_code == 200
    assert response.json()["iso_code"] == "AUT"

def test_patch_country():
    client.post("/Countries/", json={
        "name": "Austria",
        "iso_code": "AT",
        "short_code": 40
    })
    response = client.patch("/Countries/Austria", json={"short_code": 43})
    assert response.status_code == 200
    assert response.json()["short_code"] == 43

def test_delete_country():
    client.post("/Countries/", json={
        "name": "Austria",
        "iso_code": "AT",
        "short_code": 40
    })
    response = client.delete("/Countries/Austria")
    assert response.status_code == 200
    assert response.json() == {"detail": "Country 'Austria' deleted"}
    assert client.get("/Countries/Austria").status_code == 404


# ── Relationships ──────────────────────────────────────────────────────────────

def test_create_relationship():
    client.post("/Identifiers/", json={"identifier_name": "88823147", "description": "Conditioner Bottle", "identifier_type": "Finished Product Part"})
    client.post("/Identifiers/", json={"identifier_name": "88823148", "description": "Conditioner Packaging", "identifier_type": "Packaging Material Part"})
    response = client.post("/Relationships/", json={
        "from_identifier_name": "88823147",
        "to_identifier_name": "88823148",
        "relationship_name": "Contains"
    })
    assert response.status_code == 200
    assert response.json()["from_identifier_name"] == "88823147"
    assert response.json()["to_identifier_name"] == "88823148"

def test_get_relationships():
    response = client.get("/Relationships/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_relationship_not_found():
    response = client.get("/Relationships/00000000")
    assert response.status_code == 404

def test_patch_relationship():
    client.post("/Identifiers/", json={"identifier_name": "88823147", "description": "Conditioner Bottle", "identifier_type": "Finished Product Part"})
    client.post("/Identifiers/", json={"identifier_name": "88823148", "description": "Conditioner Packaging", "identifier_type": "Packaging Material Part"})
    client.post("/Relationships/", json={
        "from_identifier_name": "88823147",
        "to_identifier_name": "88823148",
        "relationship_name": "Contains"
    })
    response = client.patch("/Relationships/88823147/88823148", json={"relationship_name": "Requires"})
    assert response.status_code == 200
    assert response.json()["relationship_name"] == "Requires"

def test_delete_relationship():
    client.post("/Identifiers/", json={"identifier_name": "88823147", "description": "Conditioner Bottle", "identifier_type": "Finished Product Part"})
    client.post("/Identifiers/", json={"identifier_name": "88823148", "description": "Conditioner Packaging", "identifier_type": "Packaging Material Part"})
    client.post("/Relationships/", json={
        "from_identifier_name": "88823147",
        "to_identifier_name": "88823148",
        "relationship_name": "Contains"
    })
    response = client.delete("/Relationships/88823147/88823148")
    assert response.status_code == 200
    assert "deleted" in response.json()["detail"]


# ── Characteristics ────────────────────────────────────────────────────────────

def test_create_characteristic():
    response = client.post("/Characteristics/", json={
        "master_name": "CM-99001",
        "name": "Greutate"
    })
    assert response.status_code == 200
    assert response.json()["master_name"] == "CM-99001"
    assert response.json()["name"] == "Greutate"

def test_get_characteristics():
    response = client.get("/Characteristics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_characteristic_not_found():
    response = client.get("/Characteristics/CM-00000/Inexistent")
    assert response.status_code == 404

def test_patch_characteristic():
    client.post("/Characteristics/", json={
        "master_name": "CM-99002",
        "name": "Culoare"
    })
    response = client.patch("/Characteristics/CM-99002/Culoare", json={
        "specifics": "Culoare sampoo - transparent sau alb"
    })
    assert response.status_code == 200
    assert response.json()["specifics"] == "Culoare sampoo - transparent sau alb"

def test_delete_characteristic():
    client.post("/Characteristics/", json={
        "master_name": "CM-99001",
        "name": "Greutate"
    })
    response = client.delete("/Characteristics/CM-99001/Greutate")
    assert response.status_code == 200
    assert "deleted" in response.json()["detail"]