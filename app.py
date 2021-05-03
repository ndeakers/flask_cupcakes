"""Flask app for Cupcakes"""
from flask import Flask, url_for, render_template, redirect, flash, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def show_homepage():
    return render_template('home_page.html')


# ************* API Routes ************

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """
    Return JSON 
    {cupcakes: [{id, flavor, size, rating, image}, ...]}.
    """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """
    Return JSON 
    {cupcake: {id, flavor, size, rating, image}}.
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """
    Create cupcake from form data & return it.

    Returns JSON 
    
    {cupcake: {id, flavor, size, rating, image}}.
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake(
        flavor=flavor, 
        size=size,
        rating=rating,
        image=image
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """update cupcake details
    Input should be {
    "cupcake": {
        "flavor": "strawberry",
        "id": 1,
        "image": "http://test.com/cupcake.jpg",
        "rating": 5,
        "size": "TestSize"
    }
    }

    Respond with JSON of the newly-updated cupcake, like this: 
    {cupcake: {id, flavor, size, rating, image}}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    print(cupcake.flavor)
    print('response', request.json)

    current_cupcake = request.json['cupcake']

    cupcake.flavor = current_cupcake["flavor"]
    cupcake.size = current_cupcake["size"]
    cupcake.rating = current_cupcake["rating"]
    cupcake.image = current_cupcake["image"]

    db.session.commit()

    serialized = cupcake.serialize()
    return (jsonify(cupcake=serialized))


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete cupcake 
    Delete cupcake with the id passed in the URL.
    Respond with JSON like {message: "Deleted"}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({"message": "Deleted"})