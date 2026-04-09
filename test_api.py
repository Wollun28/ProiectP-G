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


#============Identifiers si Country===========================#


from fastapi.testclient import TestClient
import pytest
from proiect_mainapi import app, get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup():
    yield
    client.delete("/Identifiers/CNP")
    client.delete("/Countries/Romania")


def test_create_identifier():
    response = client.post("/Identifiers/", json={
        "identifier_name": "CNP",
        "description": "Cod Numeric Personal",
        "identifier_type": "Personal"
    })
    assert response.status_code == 200
    assert response.json()["identifier_name"] == "CNP"

def test_get_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "CNP",
        "description": "Cod Numeric Personal",
        "identifier_type": "Personal"
    })
    response = client.get("/Identifiers/CNP")
    assert response.status_code == 200
    assert response.json()["identifier_name"] == "CNP"

def test_get_identifier_not_found():
    response = client.get("/Identifiers/INEXISTENT")
    assert response.status_code == 404
    assert response.json() == {"detail": "Identifier not found"}

def test_put_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "CNP",
        "description": "Vechi",
        "identifier_type": "Personal"
    })
    response = client.put("/Identifiers/CNP", json={
        "identifier_name": "CNP",
        "description": "Nou",
        "identifier_type": "Personal"
    })
    assert response.status_code == 200
    assert response.json()["description"] == "Nou"

def test_patch_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "CNP",
        "description": "Original",
        "identifier_type": "Personal"
    })
    response = client.patch("/Identifiers/CNP", json={"description": "Actualizat"})
    assert response.status_code == 200
    assert response.json()["description"] == "Actualizat"

def test_delete_identifier():
    client.post("/Identifiers/", json={
        "identifier_name": "CNP",
        "description": "De sters",
        "identifier_type": "Personal"
    })
    response = client.delete("/Identifiers/CNP")
    assert response.status_code == 200
    assert response.json() == {"detail": "Identifier 'CNP' deleted"}
    assert client.get("/Identifiers/CNP").status_code == 404



def test_create_country():
    response = client.post("/Countries/", json={
        "name": "Romania",
        "iso_code": "ROU",
        "short_code": 40
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Romania"

def test_get_country():
    client.post("/Countries/", json={
        "name": "Romania",
        "iso_code": "ROU",
        "short_code": 40
    })
    response = client.get("/Countries/Romania")
    assert response.status_code == 200
    assert response.json()["name"] == "Romania"

def test_get_country_not_found():
    response = client.get("/Countries/Narnia")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}

def test_put_country():
    client.post("/Countries/", json={
        "name": "Romania",
        "iso_code": "ROU",
        "short_code": 40
    })
    response = client.put("/Countries/Romania", json={
        "name": "Romania",
        "iso_code": "ROM",
        "short_code": 40
    })
    assert response.status_code == 200
    assert response.json()["iso_code"] == "ROM"

def test_patch_country():
    client.post("/Countries/", json={
        "name": "Romania",
        "iso_code": "ROU",
        "short_code": 40
    })
    response = client.patch("/Countries/Romania", json={"iso_code": "RO"})
    assert response.status_code == 200
    assert response.json()["iso_code"] == "RO"

def test_delete_country():
    client.post("/Countries/", json={
        "name": "Romania",
        "iso_code": "ROU",
        "short_code": 40
    })
    response = client.delete("/Countries/Romania")
    assert response.status_code == 200
    assert response.json() == {"detail": "Country 'Romania' deleted"}
    assert client.get("/Countries/Romania").status_code == 404