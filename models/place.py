#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', cascade='all, delete', backref='place')
        amenities = relationship('Amenity', backref='place_amenities',
                                 secondary='place_amenity', viewonly=False)
    else:
        @property
        def reviews(self):
            """
            returns the list of Review instances with place_id equals to
            the current Place.id
            """
            reviews = storage.all(Review).values()
            return [review for review in reviews if self.id == review.id]

        @property
        def amenities(self):
            """
            returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place
            """
            from models import storage
            from models.amenity import Amenity

            amenities = storage.all(Amenity)

            amenities_list = []
            for key, value in amenities.items():
                if key in self.amenity_ids:
                    amenities_list.append(amenities[key])

            return amenities_list

        @amenities.setter
        def amenities(self, obj=None):
            """Set amenity ids"""
            if isInstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
