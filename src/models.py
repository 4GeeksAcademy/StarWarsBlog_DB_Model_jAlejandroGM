from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    subscription_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.UTC))

    favorites = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None,
        }


class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)

    favorites = relationship("Favorite", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "birth_year": self.birth_year,
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)

    favorites = relationship("Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
        }


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=True)
    vehicle_class: Mapped[str] = mapped_column(String(50), nullable=True)

    favorites = relationship("Favorite", back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "vehicle_class": self.vehicle_class,
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicle.id'), nullable=True)

    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    vehicle = relationship("Vehicle", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
        }
