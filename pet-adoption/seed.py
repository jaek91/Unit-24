"""Seed file to make sample data for db."""

from models import db, Pet

# Create all tables
db.drop_all()
db.create_all()

Pet.query.delete()

pet1 = Pet(name="Lucky", species="dog", age= 10, notes="Very energetic for his age", available=True)
pet2 = Pet(name="Porquito", species="porcupine", age=5, photo_url = "https://images.pexels.com/photos/5030891/pexels-photo-5030891.jpeg", 
notes="amazing hair", available = False)

db.session.add(pet1)
db.session.add(pet2)
db.session.commit()