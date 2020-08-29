import os
from flask import Flask, render_template, request, abort, jsonify, session
from models import *
from flask_migrate import Migrate
from flask_cors import CORS
from helper import *
from consts import *
from route_movies import add_movie_routes
from route_errors import add_error_routes

def create_app(test_config=None):

    app = Flask(__name__)
    set_up_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    add_error_routes(app=app)
    add_movie_routes(app=app)
    

    return app


app = create_app()
migrate = Migrate(app, db)


@app.after_request 
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def get_home():
    debug = False
    if app.debug:
        debug = True

    return jsonify({
        "Index": "Home", 
        "Debug": debug,
        "Database": app.config['SQLALCHEMY_DATABASE_URI']
    })


import route_auth
import route_actors

if __name__ == '__main__':
    app.run()