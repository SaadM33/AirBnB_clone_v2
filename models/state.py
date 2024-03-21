#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    if storage_type == 'db':
        cities = relationship("City", cascade="all, delete", backref="state")
        name = Column(String(128), nullable=False)
    else:
        name = ""

        @property
        def cities(self):
            """getter docuemnt"""
            from models import storage
            citiesList = []
            citiesAll = storage.all(City)
            for city in citiesAll.values():
                if city.state_id == self.id:
                    citiesList.append(city)
            return citiesList
