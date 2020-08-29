import os
from flask import Flask, render_template, request, abort, jsonify, session
from models import *
from flask_migrate import Migrate
from helper import *
from consts import *
from route_login_cors import *
from route_movies import add_movie_routes
from route_errors import add_error_routes
from route_actors import add_actor_routes

def create_app(test_config=None):

    app = Flask(__name__)
    set_up_db(app)
    
    add_cors(app=app)
    add_home_route(app=app)
    add_error_routes(app=app)
    add_login_routes(app=app)
    add_movie_routes(app=app)
    add_actor_routes(app=app)

    return app


app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()