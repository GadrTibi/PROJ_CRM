from database import db

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    teleprospector_id = db.Column(db.Integer, db.ForeignKey('teleprospector.id'), nullable=False)

class Teleprospector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    leads = db.relationship('Lead', backref='teleprospector', lazy=True)

class Manager(Teleprospector):
    teleprospectors = db.relationship('Teleprospector', backref='manager', lazy=True)
