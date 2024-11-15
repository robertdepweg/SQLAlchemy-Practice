"""Beverage data models"""

# System Imports.
import os

# Third-party imports
from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import (
    String,
    Float,
    Boolean
)

engine = create_engine("sqlite:///db.sqlite3", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Base class for other models to inherit from
Base = declarative_base()


class Beverage(Base):
    """Beverage class"""
    
    __tablename__ = "beverages"

    id = Column(String(255), primary_key=True) # TODO: no auto increment, something else?
    name = Column(String(255), nullable=False)
    pack = Column(String(255), nullable=False)
    price = Column(Float(2), nullable=False)
    active = Column(Boolean, nullable=False)

    def __init__(self, id_, name, pack, price, active):
        """Constructor"""
        self.id = id_
        self.name = name
        self.pack = pack
        self.price = price
        self.active = active

    def __str__(self):
        """String method"""
        active = "True" if self.active else "False"
        return f"| {self.id:>6} | {self.name:<56} | {self.pack:<15} | {self.price:>6.2f} | {active:<6} |"


class BeverageRepository:
    """BeverageRepository class"""

    _collection = []

    def __str__(self):
        """String method"""
        beverages = session.query(Beverage).all()
        output_string = ""
        for beverage in beverages:
            output_string += f"{beverage}{os.linesep}"
        return output_string

    def create_database(self):
        """Create the database"""
        Base.metadata.create_all(engine)

    def db_status(self):
        """Returns if database has items inside or not"""
        return session.query(Beverage).first()
    
    def populate_database(self):
        """Populate database from list of employees"""
        for bev in self._collection:
            session.add(bev)
            session.commit()

    def insert(self, id_, name, pack, price, active):
        """Add a new beverage to the collection"""
        new_beverage = Beverage(id_, name, pack, price, active)
        session.add(new_beverage)
        session.commit()

    def update(self, entry):
        """Updates beverage in database"""
        session.query(Beverage).filter(Beverage.id == entry).first()
        session.commit()

    def delete(self):
        """Deletes beverage from database"""
        beverage_to_delete = (
            session.query(
                Beverage,
            )
            .filter(
                Beverage.first_name == "David",
            )
            .first()
        )
        session.commit()

    def query_by_id(self, id):
        """Find a beverage by it's id"""
        session.query(BeverageRepository).get(id)
            
            
