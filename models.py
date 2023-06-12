from database import db

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # Ajoutez d'autres champs si nécessaire

class Teleprospector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # Ajoutez d'autres champs si nécessaire

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # Ajoutez d'autres champs si nécessaire
