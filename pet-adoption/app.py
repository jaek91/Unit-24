from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Pet
from forms import NewPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """Display home page of our pets"""
    pets = Pet.query.all()
    return render_template("home.html", pets = pets)

@app.route('/add', methods=["GET", "POST"])
def add_pets():
    """Route for adding a new pet"""
    form = NewPetForm()

    if form.validate_on_submit():
        pet_name = form.name.data
        pet_species = form.species.data
        pet_age = form.age.data
        pet_notes = form.notes.data
        new_pet = Pet(name= pet_name, species = pet_species, age = pet_age, notes = pet_notes)

        db.session.add(new_pet)
        db.session.commit()
        flash(f"Created new pet: name is {pet_name}, species is ${pet_species}")
        return redirect("/")
    else:
        return render_template("add_new_pet.html", form = form)

@app.route('/<int:pet_id>', methods=["GET", "POST"])
def see_pet_info(pet_id):
    """Route to view for more about a pet"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data 
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"Updated info for {pet.name}")
        return redirect("/")
    else:
        return render_template("edit_pet.html", form = form, pet = pet)

