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

    id = Column(String(255), primary_key=True)
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
        """Returns if database has beverages inside or not"""
        session.query(Beverage).first()
    
    def populate_database(self):
        """Populate database from list of beverages"""
        beverages = session.query(Beverage).all()
        for bev in beverages:
            session.add(bev)
            session.commit()

    def insert(self, id_, name, pack, price, active):
        """Add a new beverage to the collection"""
        new_beverage = Beverage(id_, name, pack, price, active)
        session.add(new_beverage)
        session.commit()

    def update(self, search_query, new_info):
        """Updates beverage in database"""
        beverage_to_update = (
            session.query(
                Beverage,
            )
            .filter(
                Beverage.id == search_query
            )
            .first()
        )

        beverage_to_update.id = new_info[0]
        beverage_to_update.name = new_info[1]
        beverage_to_update.pack = new_info[2]
        beverage_to_update.price = float(new_info[3])
        beverage_to_update.active = bool(new_info[4])
        session.commit()

    def delete(self, search_query):
        """Deletes beverage from database"""
        beverage_to_delete = (
            session.query(
                Beverage,
            )
            .filter(
                Beverage.id == search_query,
            )
            .first()
        )
        session.delete(beverage_to_delete)
        session.commit()

    def query_by_id(self, search_query):
        """Find a beverage by it's id"""
        single_beverage_by_critera = (
            session.query(
                Beverage,
            )
            .filter(Beverage.id == search_query,
            )
            .first()
            )
        return single_beverage_by_critera
            
            
