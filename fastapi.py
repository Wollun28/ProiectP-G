from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session,sessionmaker, declarative_base
from sqlalchemy import create_engine
from fastapi.responses import HTMLResponse
from proiect_classes import (
    Base,
    # Cele de baza:
    Identifier, Country, ConsumerUnit, Ownership,
    Relationship, Characteristic,
    # Modele fastAPI:
    IdentifierCreate, IdentifierResponse, IdentifierUpdate,
    CountryCreate, CountryResponse, CountryUpdate,
    ConsumerUnitCreate, ConsumerUnitResponse, ConsumerUnitUpdate,
    OwnershipCreate, OwnershipResponse, OwnershipUpdate,
    RelationshipCreate, RelationshipResponse, RelationshipUpdate,
    CharacteristicCreate, CharacteristicResponse, CharacteristicUpdate,

)
app = FastAPI()



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
    return """
   <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Pagina Principala | Dashboard</title>
        <style>
            body {
                background-color: #0f172a; /* Fundal bleumarin-închis modern */
                background-image: radial-gradient(circle at top right, #1e293b, #0f172a);
                color: #f8fafc;
                font-family: 'Segoe UI', Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: #1e293b;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
                text-align: center;
                border: 1px solid #334155;
                max-width: 450px;
                width: 90%;
            }
            h1 {
                color: #4ade80; /* Verde neon subtil */
                font-size: 2.2rem;
                margin-bottom: 1rem;
                font-weight: 700;
            }
            p {
                color: #94a3b8;
                font-size: 1.1rem;
                margin-bottom: 2rem;
                line-height: 1.6;
            }
            .status-badge {
                display: inline-block;
                background: rgba(74, 222, 128, 0.1);
                color: #4ade80;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                margin-bottom: 20px;
                font-weight: 600;
                border: 1px solid rgba(74, 222, 128, 0.2);
            }
            .btn {
                display: inline-block;
                padding: 14px 28px;
                background: #4ade80;
                color: #064e3b;
                text-decoration: none;
                border-radius: 12px;
                font-weight: 700;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .btn:hover {
                background: #22c55e;
                transform: translateY(-2px);
                box-shadow: 0 10px 15px -3px rgba(74, 222, 128, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="status-badge">● Sistem Online</div>
            <h1>Pagina Principala</h1>
            <p>Serverul rulează corect și este conectat cu succes la <strong>SQL Server</strong> prin MSSQL.</p>
            <a href="/docs" class="btn">
                Deschide Documentația Swagger
            </a>
        </div>
    </body>
    </html>
    """



@app.post("/Identifiers/", response_model=IdentifierResponse)
def create_identifier(identifier: IdentifierCreate, db: Session = Depends(get_db)):
    db_identifier = Identifier(**identifier.model_dump())
    db.add(db_identifier)
    db.commit()
    db.refresh(db_identifier)
    return db_identifier


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
    for key, value in identifier.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj
 
 
@app.patch("/Identifiers/{identifier_name}", response_model=IdentifierResponse)
def patch_identifier(identifier_name: str, identifier: IdentifierUpdate, db: Session = Depends(get_db)):
    obj = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    for key, value in identifier.model_dump(exclude_none=True).items():  
        ##asta e ca sa nu facem aia cu is not none de 1000 de ori
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
    for key, value in country.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj
 
 
@app.patch("/Countries/{country_name}", response_model=CountryResponse)
def patch_country(country_name: str, country: CountryUpdate, db: Session = Depends(get_db)):
    obj = db.query(Country).filter(Country.name == country_name).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Country not found")
    for key, value in country.model_dump(exclude_none=True).items():
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
    for key, value in cu.model_dump().items():
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
    for key, value in cu.model_dump(exclude_none=True).items():
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
    for key, value in ownership.model_dump().items():
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
    for key, value in ownership.model_dump(exclude_none=True).items():
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
    for key, value in rel.model_dump().items():
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
    for key, value in rel.model_dump(exclude_none=True).items():
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
    return {"detail": f"Relationship ({from_identifier_name} → {to_identifier_name}) deleted"}
 
 
 
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
    for key, value in char.model_dump().items():
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
    for key, value in char.model_dump(exclude_none=True).items():
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
 
 
