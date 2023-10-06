from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    powers = db.relationship("Power", secondary="hero_powers", back_populates="heroes")

    def __str__(self):
        return self.name

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strength = ['Strong', 'Weak', 'Average']
        if strength not in valid_strength:
            raise ValueError('Strength must either be Strong or Weak or Average')
        return strength

    def __str__(self):
        return str(self.power_id)

class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    heroes = db.relationship("Hero", secondary="hero_powers", back_populates="powers")

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description is required and must have a length of at least 20 characters")
        return description

    def __str__(self):
        return self.name
