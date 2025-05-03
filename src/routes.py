from flask import Blueprint, jsonify, request
from models import db, User, People, Planets, Vehicles, Favorites

api = Blueprint('api', __name__)

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Invalid data"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400
    new_user = User(username=data['username'])
    new_user.encrypt_pass(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@api.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@api.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = People.query.get(person_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@api.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Invalid data"}), 400
    new_person = People(
        name=data['name'],
        height=data['height'],
        mass=data['mass'],
        birth_year=data['birth_year']
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@api.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Invalid data"}), 400
    new_planet = Planets(
        name=data['name'],
        climate=data['climate'],
        terrain=data['terrain'],
        population=data['population']
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    favorites = Favorites.query.filter_by(user_id=user.id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"message": "Invalid data"}), 400
    user_id = data['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    already_favorited = Favorites.query.filter_by(user_id=user_id, planets_id=planet_id).first()
    if already_favorited:
        return jsonify({"message": "Planet already favorited"}), 400
    favorite = Favorites(user_id=user_id, planets_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@api.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"message": "Invalid data"}), 400
    user_id = data['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    person = People.query.get(person_id)
    if not person:
        return jsonify({"message": "Person not found"}), 404
    already_favorited = Favorites.query.filter_by(user_id=user_id, people_id=person_id).first()
    if already_favorited:
        return jsonify({"message": "Person already favorited"}), 400
    favorite = Favorites(user_id=user_id, people_id=person_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"message": "Invalid data"}), 400
    user_id = data['user_id']
    favorite = Favorites.query.filter_by(user_id=user_id, planets_id=planet_id).first()
    if not favorite:
        return jsonify({"message": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 200

@api.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"message": "Invalid data"}), 400
    user_id = data['user_id']
    favorite = Favorites.query.filter_by(user_id=user_id, people_id=person_id).first()
    if not favorite:
        return jsonify({"message": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 200