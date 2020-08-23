from casting_agency_app import app
from models import * 
from flask import Flask, render_template, request, abort, jsonify, session
from helper import *

# create a movie
@app.route('/api/movie', methods=['POST'])
def create_a_movie():
    payload = request.json

    if 'title' not in payload or 'release_date' not in payload:
        abort(422)
    
    success = True
    try:
        date = format_datetime(payload['release_date'])
        print("Release date: ", date)

        movie = Movies(title=payload['title'], 
                       release_date=date)
        
        db.session.add(movie)
        db.session.commit()
    except():
        abort(500)
        success = False
    finally:
        db.session.close()

    return jsonify({
            "success": success,
            "movie": payload
            })


# get a list of all movies
@app.route('/api/movies')
def get_movies():
    movies = []

    raw_moives = Movies.query.all()

    if len(raw_moives) > 0:
        for movie in raw_moives:
            movies.append(movie.format())
    
    return jsonify({
        "success": True, 
        "movies": movies
    })

