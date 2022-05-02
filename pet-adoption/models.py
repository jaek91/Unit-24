from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """Pet class description"""

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.Text,
                     nullable=False)
    species = db.Column(db.Text,
                     nullable=False)

    photo_url = db.Column(db.Text, nullable=False, default ="https://www.publicdomainpictures.net/pictures/50000/velka/paw-prints.jpg")
    age = db.Column(db.Integer)

    notes = db.Column(db.Text)

    available = db.Column(db.Boolean, nullable=False, default = True)  