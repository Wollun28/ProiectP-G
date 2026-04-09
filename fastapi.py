from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from proiect_classes import (
    Base,
    Identifier, Country, ConsumerUnit, Ownership,
    Relationship, Characteristic,
    IdentifierCreate, IdentifierResponse, IdentifierUpdate,
    CountryCreate, CountryResponse, CountryUpdate,
    ConsumerUnitCreate, ConsumerUnitResponse, ConsumerUnitUpdate,
    OwnershipCreate, OwnershipResponse, OwnershipUpdate,
    RelationshipCreate, RelationshipResponse, RelationshipUpdate,
    CharacteristicCreate, CharacteristicResponse, CharacteristicUpdate,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = 'mssql+pyodbc://GREEN/Proiect?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()


# ─── IDENTIFIERS ─────────────────────────────────────────────────────────────


@app.post("/Identifiers/", response_model=IdentifierResponse)
def create_identifier(identifier: IdentifierCreate, db: Session = Depends(get_db)):
    db_obj = Identifier(**identifier.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/Identifiers/", response_model=list[IdentifierResponse])
def read_all_identifiers(db: Session = Depends(get_db)):
    return db.query(Identifier).all()

@app.get("/Identifiers/{identifier_name}", response_model=IdentifierResponse)
def read_identifier(identifier_name: str, db: Session = Depends(get_db)):
    obj = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    return obj

@app.put("/Identifiers/{identifier_name}", response_model=IdentifierResponse)
def update_identifier(identifier_name: str, identifier: IdentifierCreate, db: Session = Depends(get_db)):
    obj = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    data = identifier.model_dump()
    data.pop("identifier_name", None)  # nu modifica cheia primara
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.patch("/Identifiers/{identifier_name}", response_model=IdentifierResponse)
def patch_identifier(identifier_name: str, identifier: IdentifierUpdate, db: Session = Depends(get_db)):
    obj = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    data = identifier.model_dump(exclude_none=True)
    data.pop("identifier_name", None)  
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/Identifiers/{identifier_name}")
def delete_identifier(identifier_name: str, db: Session = Depends(get_db)):
    obj = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    db.delete(obj)
    db.commit()
    return {"detail": f"Identifier '{identifier_name}' deleted"}


# ─── COUNTRIES ───────────────────────────────────────────────────────────────


@app.post("/Countries/", response_model=CountryResponse)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    db_obj = Country(**country.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/Countries/", response_model=list[CountryResponse])
def read_all_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()

@app.get("/Countries/{country_name}", response_model=CountryResponse)
def read_country(country_name: str, db: Session = Depends(get_db)):
    obj = db.query(Country).filter(Country.name == country_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return obj

@app.put("/Countries/{country_name}", response_model=CountryResponse)
def update_country(country_name: str, country: CountryCreate, db: Session = Depends(get_db)):
    obj = db.query(Country).filter(Country.name == country_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Country not found")
    data = country.model_dump()
    data.pop("name", None)  
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.patch("/Countries/{country_name}", response_model=CountryResponse)
def patch_country(country_name: str, country: CountryUpdate, db: Session = Depends(get_db)):
    obj = db.query(Country).filter(Country.name == country_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Country not found")
    data = country.model_dump(exclude_none=True)
    data.pop("name", None)  
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/Countries/{country_name}")
def delete_country(country_name: str, db: Session = Depends(get_db)):
    obj = db.query(Country).filter(Country.name == country_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Country not found")
    db.delete(obj)
    db.commit()
    return {"detail": f"Country '{country_name}' deleted"}


# ─── CONSUMER UNITS ──────────────────────────────────────────────────────────


@app.post("/ConsumerUnits/", response_model=ConsumerUnitResponse)
def create_consumer_unit(cu: ConsumerUnitCreate, db: Session = Depends(get_db)):
    db_obj = ConsumerUnit(**cu.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/ConsumerUnits/", response_model=list[ConsumerUnitResponse])
def read_all_consumer_units(db: Session = Depends(get_db)):
    return db.query(ConsumerUnit).all()

@app.get("/ConsumerUnits/{country_name}", response_model=list[ConsumerUnitResponse])
def read_consumer_units_by_country(country_name: str, db: Session = Depends(get_db)):
    objs = db.query(ConsumerUnit).filter(ConsumerUnit.country_name == country_name).all()
    if not objs:
        raise HTTPException(status_code=404, detail="No consumer units found for this country")
    return objs

@app.put("/ConsumerUnits/{country_name}/{number_of_consumers}", response_model=ConsumerUnitResponse)
def update_consumer_unit(country_name: str, number_of_consumers: int, cu: ConsumerUnitCreate, db: Session = Depends(get_db)):
    obj = db.query(ConsumerUnit).filter(
        ConsumerUnit.country_name == country_name,
        ConsumerUnit.number_of_consumers == number_of_consumers
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="ConsumerUnit not found")
    data = cu.model_dump()
    data.pop("country_name", None)          
    data.pop("number_of_consumers", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.patch("/ConsumerUnits/{country_name}/{number_of_consumers}", response_model=ConsumerUnitResponse)
def patch_consumer_unit(country_name: str, number_of_consumers: int, cu: ConsumerUnitUpdate, db: Session = Depends(get_db)):
    obj = db.query(ConsumerUnit).filter(
        ConsumerUnit.country_name == country_name,
        ConsumerUnit.number_of_consumers == number_of_consumers
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="ConsumerUnit not found")
    data = cu.model_dump(exclude_none=True)
    data.pop("country_name", None)
    data.pop("number_of_consumers", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/ConsumerUnits/{country_name}/{number_of_consumers}")
def delete_consumer_unit(country_name: str, number_of_consumers: int, db: Session = Depends(get_db)):
    obj = db.query(ConsumerUnit).filter(
        ConsumerUnit.country_name == country_name,
        ConsumerUnit.number_of_consumers == number_of_consumers
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="ConsumerUnit not found")
    db.delete(obj)
    db.commit()
    return {"detail": f"ConsumerUnit ({country_name}, {number_of_consumers}) deleted"}


# ─── OWNERSHIP ───────────────────────────────────────────────────────────────


@app.post("/Ownership/", response_model=OwnershipResponse)
def create_ownership(ownership: OwnershipCreate, db: Session = Depends(get_db)):
    db_obj = Ownership(**ownership.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/Ownership/", response_model=list[OwnershipResponse])
def read_all_ownerships(db: Session = Depends(get_db)):
    return db.query(Ownership).all()

@app.get("/Ownership/{identifier_name}", response_model=list[OwnershipResponse])
def read_ownership_by_identifier(identifier_name: str, db: Session = Depends(get_db)):
    objs = db.query(Ownership).filter(Ownership.identifier_name == identifier_name).all()
    if not objs:
        raise HTTPException(status_code=404, detail="Ownership not found for this identifier")
    return objs

@app.put("/Ownership/{identifier_name}/{user_id_tnumber}", response_model=OwnershipResponse)
def update_ownership(identifier_name: str, user_id_tnumber: str, ownership: OwnershipCreate, db: Session = Depends(get_db)):
    obj = db.query(Ownership).filter(
        Ownership.identifier_name == identifier_name,
        Ownership.user_id_tnumber == user_id_tnumber
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Ownership not found")
    data = ownership.model_dump()
    data.pop("identifier_name", None)   
    data.pop("user_id_tnumber", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.patch("/Ownership/{identifier_name}/{user_id_tnumber}", response_model=OwnershipResponse)
def patch_ownership(identifier_name: str, user_id_tnumber: str, ownership: OwnershipUpdate, db: Session = Depends(get_db)):
    obj = db.query(Ownership).filter(
        Ownership.identifier_name == identifier_name,
        Ownership.user_id_tnumber == user_id_tnumber
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Ownership not found")
    data = ownership.model_dump(exclude_none=True)
    # OwnershipUpdate nu are chei primare, dar le scoatem preventiv
    data.pop("identifier_name", None)
    data.pop("user_id_tnumber", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/Ownership/{identifier_name}/{user_id_tnumber}")
def delete_ownership(identifier_name: str, user_id_tnumber: str, db: Session = Depends(get_db)):
    obj = db.query(Ownership).filter(
        Ownership.identifier_name == identifier_name,
        Ownership.user_id_tnumber == user_id_tnumber
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Ownership not found")
    db.delete(obj)
    db.commit()
    return {"detail": f"Ownership ({identifier_name}, {user_id_tnumber}) deleted"}


# ─── RELATIONSHIPS ───────────────────────────────────────────────────────────


@app.post("/Relationships/", response_model=RelationshipResponse)
def create_relationship(rel: RelationshipCreate, db: Session = Depends(get_db)):
    db_obj = Relationship(**rel.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/Relationships/", response_model=list[RelationshipResponse])
def read_all_relationships(db: Session = Depends(get_db)):
    return db.query(Relationship).all()

@app.get("/Relationships/{from_identifier_name}", response_model=list[RelationshipResponse])
def read_relationships_from(from_identifier_name: str, db: Session = Depends(get_db)):
    objs = db.query(Relationship).filter(Relationship.from_identifier_name == from_identifier_name).all()
    if not objs:
        raise HTTPException(status_code=404, detail="No relationships found for this identifier")
    return objs

@app.put("/Relationships/{from_identifier_name}/{to_identifier_name}", response_model=RelationshipResponse)
def update_relationship(from_identifier_name: str, to_identifier_name: str, rel: RelationshipCreate, db: Session = Depends(get_db)):
    obj = db.query(Relationship).filter(
        Relationship.from_identifier_name == from_identifier_name,
        Relationship.to_identifier_name == to_identifier_name
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    data = rel.model_dump()
    data.pop("from_identifier_name", None)  # nu modifica cheile primare
    data.pop("to_identifier_name", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.patch("/Relationships/{from_identifier_name}/{to_identifier_name}", response_model=RelationshipResponse)
def patch_relationship(from_identifier_name: str, to_identifier_name: str, rel: RelationshipUpdate, db: Session = Depends(get_db)):
    obj = db.query(Relationship).filter(
        Relationship.from_identifier_name == from_identifier_name,
        Relationship.to_identifier_name == to_identifier_name
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    data = rel.model_dump(exclude_none=True)
    data.pop("from_identifier_name", None)
    data.pop("to_identifier_name", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/Relationships/{from_identifier_name}/{to_identifier_name}")
def delete_relationship(from_identifier_name: str, to_identifier_name: str, db: Session = Depends(get_db)):
    obj = db.query(Relationship).filter(
        Relationship.from_identifier_name == from_identifier_name,
        Relationship.to_identifier_name == to_identifier_name
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    db.delete(obj)
    db.commit()
    return {"detail": f"Relationship ({from_identifier_name} -> {to_identifier_name}) deleted"}


# ─── CHARACTERISTICS ─────────────────────────────────────────────────────────


@app.post("/Characteristics/", response_model=CharacteristicResponse)
def create_characteristic(char: CharacteristicCreate, db: Session = Depends(get_db)):
    db_obj = Characteristic(**char.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/Characteristics/", response_model=list[CharacteristicResponse])
def read_all_characteristics(db: Session = Depends(get_db)):
    return db.query(Characteristic).all()

@app.get("/Characteristics/{master_name}", response_model=list[CharacteristicResponse])
def read_characteristics_by_master(master_name: str, db: Session = Depends(get_db)):
    objs = db.query(Characteristic).filter(Characteristic.master_name == master_name).all()
    if not objs:
        raise HTTPException(status_code=404, detail="No characteristics found for this master")
    return objs

@app.get("/Characteristics/{master_name}/{name}", response_model=CharacteristicResponse)
def read_characteristic(master_name: str, name: str, db: Session = Depends(get_db)):
    obj = db.query(Characteristic).filter(
        Characteristic.master_name == master_name,
        Characteristic.name == name
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Characteristic not found")
    return obj

@app.put("/Characteristics/{master_name}/{name}", response_model=CharacteristicResponse)
def update_characteristic(master_name: str, name: str, char: CharacteristicCreate, db: Session = Depends(get_db)):
    obj = db.query(Characteristic).filter(
        Characteristic.master_name == master_name,
        Characteristic.name == name
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Characteristic not found")
    data = char.model_dump()
    data.pop("master_name", None)  
    data.pop("name", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.patch("/Characteristics/{master_name}/{name}", response_model=CharacteristicResponse)
def patch_characteristic(master_name: str, name: str, char: CharacteristicUpdate, db: Session = Depends(get_db)):
    obj = db.query(Characteristic).filter(
        Characteristic.master_name == master_name,
        Characteristic.name == name
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Characteristic not found")
    data = char.model_dump(exclude_none=True)
    data.pop("master_name", None)
    data.pop("name", None)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/Characteristics/{master_name}/{name}")
def delete_characteristic(master_name: str, name: str, db: Session = Depends(get_db)):
    obj = db.query(Characteristic).filter(
        Characteristic.master_name == master_name,
        Characteristic.name == name
    ).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Characteristic not found")
    db.delete(obj)
    db.commit()
    return {"detail": f"Characteristic ({master_name}, {name}) deleted"}