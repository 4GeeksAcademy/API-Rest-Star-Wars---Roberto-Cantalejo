from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, LargeBinary
from passlib.hash import bcrypt_sha256
from typing import Optional, List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.LargeBinary, nullable=True)
    favorites = db.relationship("Favorites", back_populates="user")
    def encrypt_pass(self, raw_pass: str) -> None:
        self.password = bcrypt_sha256.hash(raw_pass)
    def verify_pass(self, raw_pass: str) -> bool:
        return bcrypt_sha256.verify(raw_pass, self.password)
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.String(120), nullable=False)
    mass = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    favorites = db.relationship("Favorites", back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "birth_year": self.birth_year,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    favorites = db.relationship("Favorites", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(120), nullable=False)
    manufacturer = db.Column(db.String(120), nullable=False)
    cost = db.Column(db.String(120), nullable=False)
    favorites = db.relationship("Favorites", back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost": self.cost,
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True)
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=True)
    vehicles_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=True)

    user = db.relationship("User", back_populates="favorites")
    people = db.relationship("People", back_populates="favorites")
    planet = db.relationship("Planets", back_populates="favorites")
    vehicles = db.relationship("Vehicles", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planets_id": self.planets_id,
            "vehicles_id": self.vehicles_id,
        }