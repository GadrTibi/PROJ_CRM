from database import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

class Teleprospector(User):
    __tablename__ = 'teleprospectors'

    id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    leads = relationship('Lead', backref='teleprospector', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity':'teleprospector',
    }

class Manager(Teleprospector):
    __tablename__ = 'managers'

    id = db.Column(db.Integer, ForeignKey('teleprospectors.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'manager',
    }

class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    own_state = db.Column(db.String(100), nullable=False)
    chauffage = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(100), nullable=False)
    type_habitation = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    teleprospector_id = db.Column(db.Integer, ForeignKey('teleprospectors.id'), nullable=False)
