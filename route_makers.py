from flask import Flask, render_template, request, abort, jsonify, session
from helper import *
from auth import *
from models import *

def add_movie_routes(app):
    
    # Get a list of all movies
    @app.route('/api/movies', methods=['GET'])
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
    
    return