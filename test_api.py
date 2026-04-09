import pytest
from fastapi.testclient import TestClient
from fastapi import app

@pytest.fixture
def client():
    return TestClient(app)



####teste relationship####

def test_create_relationship(client):
    response = client.post("/Relationships/", json={
        "from_identifier_name":"A",
        "to_identifier_name":"B"
    })
    assert response.status_code == 200
    data=response.json()
    assert data["from_identifier_name"] == "A"
    assert data["to_identifier_name"] == "B"

def test_get_reationships(client):
    client.post("/Relationships/", json={
        "from_identifier_name": "X",
        "to_identifier_name": "Y"
    })
    response = client.get("/Relationships/")
    assert response.status_code == 200
    assert isinstance(response.json(),list)

def test_relationship_not_found(client):
    response = client.get("/Relationships/NU_EXISTA")
    assert response.status_code == 404
    
def test_patch_relationship(client):
    client.post("/Relationships/",json={
        "from_indentifier_name": "G",
        "to_identifier_name": "H"
    })
    response = client.patch("/Relationship/G/H", json={
        "to_identifier_name":"H_modificat"
    })

    assert response.status_code == 200
    assert response.json()["to_identifier_name"] == "H_modificat"

def test_delete_relationship(client):
    client.post("/Relationship/", Json={
        "from_identiier_name": "I",
        "to_identifier_name": "J"
    })
    response = client.delete("/Relationship/I/J")
    assert response.status_code == 200
    assert "deleted" in response.json()["detail"]

####teste characteristic####

def test_create_characteristic(client):
    response = client.post("/Characteristics/", json={
        "master_name": "produs1",
        "name": "culoare"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["master_name"] == "produs1"
    assert data["name"] == "culoare"

def test_get_characteristics(client):
    response = client.get("/Characteristics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_characteristic_not_found(client):
    response = client.get("/Characteristics/x/y")
    assert response.status_code == 404

def test_patch_characteristic(client):
    client.post("/Characteristics/", json={
        "master_name": "produs5",
        "name": "culoare"
    })

    response = client.patch("/Characteristics/produs5/culoare", json={
        "name": "culoare_noua"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "culoare_noua"


def test_delete_characteristic(client):
    client.post("/Characteristics/", json={
        "master_name": "produs6",
        "name": "test"
    })

    response = client.delete("/Characteristics/produs6/test")
    assert response.status_code == 200
    assert "deleted" in response.json()["detail"]

