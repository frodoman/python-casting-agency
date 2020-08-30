from models import * 
from flask import Flask, render_template, request, abort, jsonify, session
from helper import *
from auth import *

# Add Movies endpoints to the main app
def add_movie_routes(app:Flask):

    # Create a movie
    @app.route('/api/movies/create', methods=['POST'])
    @requires_auth(Permission.POST_MOVIES)
    def create_a_movie(jwt):
        payload = request.json

        if not Movies.is_valide_payload(payload):
            abort(422)
        
        success = True
        try:
            date = format_datetime(payload['release_date'])
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


    # Search movies by name
    @app.route('/api/movies/search', methods=['POST'])
    def search_movies():
        params = request.json
        if not 'title' in params:
            abort(422)

        search_phase = "%" + params['title'] + "%"

        movies = []
        found = Movies.query.filter(Movies.title.ilike(search_phase)).order_by(Movies.title).all()
        if len(found) > 0: 
            for movie in found:
                movies.append(movie.format())
        
        return jsonify({
            "success": True, 
            "movies": movies
        })


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



    # Get a movie by id
    @app.route('/api/movies/<int:movie_id>', methods=['GET'])
    @requires_auth(Permission.READ_MOVIES)
    def get_a_movie(jwt, movie_id):
        found = {}
        movie = Movies.query.get(movie_id)

        if movie is not None:
            found = movie.format()
            return jsonify({
                "success": True, 
                "movie": found
            })
        else: 
            abort(404)


    # Update a movie
    @app.route('/api/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(Permission.PATCH_MOVIES)
    def update_a_movie(jwt, movie_id):
        payload = request.json

        if not Movies.is_valide_payload(payload):
            abort(422)
        
        success = True
        try:
            target_movie = Movies.query.get(movie_id)
            if target_movie is None:
                abort(404)

            date = format_datetime(payload['release_date'])
            target_movie.release_date = date 

            target_movie.title = payload['title']

            # link actors
            if 'actors' in payload:
                actor_ids = payload['actors']

                for actor_id in actor_ids:
                    actor = Actors.query.get(actor_id)
                    if actor is not None:
                        target_movie.actors.append(actor)

            db.session.commit()
        except():
            abort(500)
            success = False
        finally:
            db.session.close()

        return jsonify({
                "update": success,
                "movie": payload,
                "movie_id": movie_id
                })


    # Delete a movie
    @app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(Permission.DELETE_MOVIES)
    def delete_a_movie(jwt, movie_id):
        movie = Movies.query.get(movie_id)

        if movie is None:
            abort(404)
        
        success = True
        try:
            actors = movie.actors
            if len(actors) > 0:
                for actor in actors:
                    movie.actors.remove(actor)
            
            db.session.delete(movie)
            db.session.commit()
        except():
            abort(500)
            success = False
        finally:
            db.session.close()

        return jsonify({
                "delete": success,
                "movie_id": movie_id
                })

    # end of add_movie_routes
    return