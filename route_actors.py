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
            actors.append(actor.format())
    
    return jsonify({
        "success": True, 
        "actors": actors
    })