from sqlalchemy import create_engine, Column, Integer, String, Sequence,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

Base=declarative_base()


#CLASE DE BAZA
class Identifier(Base):
    _tablename_ = 'Identifiers'
    
    identifier_name = Column(String(255), primary_key=True)
    description = Column(String(255))
    identifier_type = Column(String(255))

class Country(Base):
    _tablename_ = 'Countries'
    name = Column(String(255),primary_key=True)
    iso_code = Column(String(255))
    short_code = Column(Integer)

class ConsumerUnit(Base):
    _tablename_ = 'ConsumerUnits'
    
    number_of_consumers = Column(Integer, primary_key=True)
    country_name = Column(String(255), ForeignKey('Countries.name'), primary_key=True)
    country = relationship('Country', back_populates='consumer_units')

Country.consumer_units = relationship('ConsumerUnit', order_by=ConsumerUnit.number_of_consumers, back_populates='country')

class Ownership(Base):
    _tablename_ = 'Ownership'
    
    identifier_name = Column(String(255), ForeignKey('Identifiers.identifier_name'), primary_key=True)
    originator_first_name = Column(String(255))
    originator_last_name = Column(String(255))
    user_id_tnumber = Column(String(255), primary_key=True)
    user_id_intranet = Column(String(255))
    email = Column(String(255))
    owner_first_name = Column(String(255))
    owner_last_name = Column(String(255))
    identifier = relationship('Identifier')

class Relationship(Base):
    _tablename_ = 'Relationships'
    
    from_identifier_name = Column(String(255), ForeignKey('Identifiers.identifier_name'), primary_key=True)
    to_identifier_name = Column(String(255), ForeignKey('Identifiers.identifier_name'), primary_key=True)
    relationship_name = Column(String(255))
    from_identifier = relationship('Identifier', foreign_keys=[from_identifier_name])
    to_identifier = relationship('Identifier', foreign_keys=[to_identifier_name])

class Characteristic(Base):
    _tablename_ = 'Characteristics'
    
    master_name = Column(String(255), primary_key=True)
    name = Column(String(255), primary_key=True)
    specifics = Column(String(255))
    action_required = Column(String(255))
    report_type = Column(String(255))
    data_type = Column(String(255))
    lower_routine_release_limit = Column(DECIMAL(10, 2))
    lower_limit = Column(DECIMAL(10, 2))
    lower_target = Column(DECIMAL(10, 2))
    target = Column(DECIMAL(10, 2))
    upper_target = Column(DECIMAL(10, 2))
    upper_limit = Column(DECIMAL(10, 2))
    upper_routine_release_limit = Column(DECIMAL(10, 2))
    test_frequency = Column(Integer)
    precision = Column(Integer)
    engineering_unit = Column(String(255))

class IdentifierCharacteristic(Base):
    _tablename_ = 'IdentifierCharacteristics'
    
    identifier_name = Column(String(255), ForeignKey('Identifiers.identifier_name'), primary_key=True)
    master_name = Column(String(255), ForeignKey('Characteristics.master_name'), primary_key=True)
    characteristic_name = Column(String(255), ForeignKey('Characteristics.name'), primary_key=True)
    identifier = relationship('Identifier')
    characteristic = relationship('Characteristic', primaryjoin="and_(IdentifierCharacteristic.master_name==Characteristic.master_name, 			IdentifierCharacteristic.characteristic_name==Characteristic.name)")
    

# MODELELE FASTAIP:

class IdentifierCreate(BaseModel):
    identifier_name: str
    description: str
    identifier_type: str


class IdentifierResponse(BaseModel):

    identifier_name: str
    description: str
    identifier_type: str

    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy models

class IdentifierUpdate(BaseModel):
    identifier_name: Optional[str] = None
    description: Optional[str] = None
    identifier_type: Optional[str] = None
    

class CountryCreate(BaseModel):
    name: str
    iso_code: str
    short_code: int

class CountryResponse(BaseModel):
    name: str
    iso_code: str
    short_code: int

    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy models

class CountryUpdate(BaseModel):
    name: Optional[str] = None
    iso_code: Optional[str] = None
    short_code: Optional[int] = None
    
    
    
    
class ConsumerUnitCreate(BaseModel):
    number_of_consumers: int
    country_name: str
 
class ConsumerUnitResponse(BaseModel):
    number_of_consumers: int
    country_name: str
 
    class Config:
        from_attributes = True
 
class ConsumerUnitUpdate(BaseModel):
    number_of_consumers: Optional[int] = None
    country_name:        Optional[str] = None
    

    
    
class OwnershipCreate(BaseModel):
    identifier_name:str
    originator_first_name: str
    originator_last_name:str
    user_id_tnumber:str
    user_id_intranet: str
    email: str
    owner_first_name:str
    owner_last_name:str
 
class OwnershipResponse(BaseModel):
    identifier_name: str
    originator_first_name: str
    originator_last_name:  str
    user_id_tnumber: str
    user_id_intranet: str
    email:str
    owner_first_name: str
    owner_last_name:str
 
    class Config:
        from_attributes = True
 
class OwnershipUpdate(BaseModel):
    originator_first_name: Optional[str] = None
    originator_last_name:  Optional[str] = None
    user_id_intranet: Optional[str] = None
    email: Optional[str] = None
    owner_first_name: Optional[str] = None
    owner_last_name: Optional[str] = None
    
    
class RelationshipCreate(BaseModel):
    from_identifier_name: str
    to_identifier_name: str
    relationship_name:str
 
class RelationshipResponse(BaseModel):
    from_identifier_name: str
    to_identifier_name:str
    relationship_name:str
 
    class Config:
        from_attributes = True
 
 
class RelationshipUpdate(BaseModel):
    relationship_name: Optional[str] = None 
    
    
class CharacteristicCreate(BaseModel):
    master_name: str
    name:str
    specifics:Optional[str] = None
    action_required: Optional[str] = None
    report_type: Optional[str] = None
    data_type: Optional[str] = None
    lower_routine_release_limit: Optional[Decimal] = None
    lower_limit:Optional[Decimal] = None
    lower_target:  Optional[Decimal] = None
    target:  Optional[Decimal] = None
    upper_target:  Optional[Decimal] = None
    upper_limit:   Optional[Decimal] = None
    upper_routine_release_limit: Optional[Decimal] = None
    test_frequency:   Optional[int] = None
    precision:    Optional[int] = None
    engineering_unit: Optional[str] = None
 
class CharacteristicResponse(BaseModel):
    master_name:str
    name: str
    specifics: Optional[str] = None
    action_required:Optional[str] = None
    report_type: Optional[str] = None
    data_type: Optional[str]  = None
    lower_routine_release_limit: Optional[Decimal] = None
    lower_limit: Optional[Decimal] = None
    lower_target: Optional[Decimal] = None
    target: Optional[Decimal] = None
    upper_target:Optional[Decimal] = None
    upper_limit: Optional[Decimal] = None
    upper_routine_release_limit: Optional[Decimal] = None
    test_frequency: Optional[int] = None
    precision:Optional[int] = None
    engineering_unit: Optional[str] = None
 
    class Config:
        from_attributes = True
 
class CharacteristicUpdate(BaseModel):
    specifics:Optional[str] = None
    action_required: Optional[str] = None
    report_type: Optional[str] = None
    data_type: Optional[str] = None
    lower_routine_release_limit: Optional[Decimal] = None
    lower_limit: Optional[Decimal] = None
    lower_target: Optional[Decimal] = None
    target:Optional[Decimal] = None
    upper_target:Optional[Decimal] = None
    upper_limit: Optional[Decimal] = None
    upper_routine_release_limit: Optional[Decimal] = None
    test_frequency: Optional[int] = None
    precision:  Optional[int] = None
    engineering_unit: Optional[str] = None