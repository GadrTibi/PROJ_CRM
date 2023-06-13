from database import db
from sqlalchemy.orm import relationship

class Teleprospector(db.Model):
    __tablename__ = 'teleprospectors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    leads = relationship('Lead', backref='teleprospector', lazy=True)

class Manager(Teleprospector):
    __tablename__ = 'managers'

    id = db.Column(db.Integer, db.ForeignKey('teleprospectors.id'), primary_key=True)
    teleprospectors = relationship('Teleprospector', backref='manager', lazy=True)

class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    teleprospector_id = db.Column(db.Integer, db.ForeignKey('teleprospectors.id'), nullable=False)
