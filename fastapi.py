from fastapi import FastAPI, Depends, HTTPException
from database import Product, ProductCreate, ProductResponse, ProductUpdate   
from sqlalchemy.orm import Session,sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from proiect_classes import Identifier,Country,ConsumerUnit,Ownership,Characteristic,Relationship,IdentifierCharacteristic
from proiect_classes import IdentifierCreate,IdentifierResponse,IdentifierUpdate,CountryCreate,CountryResponse,CountryUpdate

app = FastAPI()

from fastapi.responses import HTMLResponse

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
        <title>Catalog Produse | Dashboard</title>
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
            <h1>Catalog Produse</h1>
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

@app.post("/Countries/", response_model=CountryResponse)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    db_country = Country(**country.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

@app.get("/Countries/", response_model=list[CountryResponse])
def read_all_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()  
    return countries 

@app.get("/Countries/{country_id}", response_model=CountryResponse)
def read_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(Country).filter(Country.id == country_id).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@app.put("/Countries/{country_id}", response_model=CountryResponse)
def update_country(country_id: int, country: CountryCreate, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    
    
    for key, value in country.model_dump().items():
        setattr(db_country, key, value)
    
    db.commit()
    db.refresh(db_country)
    return db_country

@app.patch("/Countries/{country_id}", response_model=CountryResponse)
def patch_country(country_id: int, country_update: CountryUpdate, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    # Update only the fields that were provided in the request
    if country_update.name is not None:
        db_country.name = country_update.name
    if country_update.iso_code is not None:
        db_country.iso_code = country_update.iso_code
    if country_update.short_code is not None:
        db_country.short_code = country_update.short_code

    db.commit()
    db.refresh(db_country)
    return db_country

@app.delete("/Countries/{country_id}")
def delete_country(country_id: int, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    
    db.delete(db_country)
    db.commit()
    return {"detail": "Country deleted"}
