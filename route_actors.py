from casting_agency_app import app
from models import * 
from flask import Flask, render_template, request, abort, jsonify, session
from helper import *

# Create an actor
@app.route('/api/actor', methods=['POST'])
def create_an_actor():
    payload = request.json

    if not Actors.is_valide_payload(payload):
        abort(422)
    
    success = True
    try:
        actor = Actors(name=payload['name'], 
                       age=payload['age'],
                       gender=payload['gender'])
        
        db.session.add(actor)
        db.session.commit()
    except():
        abort(500)
        success = False
    finally:
        db.session.close()

    return jsonify({
            "success": success,
            "actor": payload
            })


# Get a list of all actors
@app.route('/api/actors')
def get_actors():
    actors = []

    raw_actors = Actors.query.all()
    if len(raw_actors) > 0:
        for actor in raw_actors:
            info = actor.format()
            if len(actor.movies) > 0:
                movies = [movie.id for movie in actor.movies]
                info["movies"] = movies

            actors.append(info)
    
    return jsonify({
        "success": True, 
        "actors": actors
    })


# Get an actor by id
@app.route('/api/actors/<int:actor_id>')
def get_an_actor(actor_id):
    found = {}
    actor = Actors.query.get(actor_id)

    if actor is not None:
        found = actor.format()
    
    return jsonify({
        "success": True, 
        "actor": found
    })


# Update an actor
@app.route('/api/actors/<int:actor_id>', methods=['PATCH'])
def update_an_actor(actor_id):
    payload = request.json

    if not Actors.is_valide_payload(payload):
        abort(422)
    
    success = True
    try:
        target_actor = Actors.query.get(actor_id)
        if target_actor is None:
            abort(404)

        target_actor.name = payload['name']
        target_actor.age = payload['age']
        target_actor.gender = payload['gender']

        # link movies
        if 'movies' in payload:
            movie_ids = payload['movies']

            for movie_id in movie_ids:
                movie = Movies.query.get(movie_id)
                if movie is not None:
                    target_actor.movies.append(movie)

        db.session.commit()
    except():
        abort(500)
        success = False
    finally:
        db.session.close()

    return jsonify({
            "update": success,
            "actor": payload,
            "actor_id": actor_id
            })


# Delete an actor
@app.route('/api/actors/<int:actor_id>', methods=['DELETE'])
def delete_an_actor(actor_id):
    actor = Actors.query.get(actor_id)

    if actor is None:
        abort(404)
    
    success = True
    try:
        movies = actor.movies
        if len(movies) > 0:
            for movie in movies:
                actor.movies.remove(movie)
        
        db.session.delete(actor)
        db.session.commit()
    except():
        abort(500)
        success = False
    finally:
        db.session.close()

    return jsonify({
            "delete": success,
            "actor_id": actor_id
            })