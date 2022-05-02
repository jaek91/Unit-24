from flask import Flask, request, jsonify, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Cupcake
# from forms import NewPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "highly-secret-pw"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.route('/api/cupcakes', methods=["GET", "POST"])
def get_or_post_cupcakes():
    if request.method == "GET":
        cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes = cupcakes)

    else: 
        """We post the new cupcake for the POST request"""
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]
        image = request.json["image"] or None
        new_cupcake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)

        db.session.add(new_cupcake)
        db.session.commit()
        response_json = jsonify(cupcake = new_cupcake.serialize())
        return (response_json, 201)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id).serialize()
    return jsonify(cupcake = cupcake)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted the cupcake!")