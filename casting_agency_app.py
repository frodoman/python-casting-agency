import os
from flask import Flask, render_template, request, abort, jsonify, session
from models import *
from flask_migrate import Migrate
from flask_cors import CORS
from helper import *

def create_app(test_config=None):

    app = Flask(__name__)
    set_up_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request 
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    return app

app = create_app()
migrate = Migrate(app, db)

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

@app.route('/api/login')
def login():
    return render_template('login.html', call_back_url="https://www.a.com/")

@app.route('/api/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/api/login-result', methods=['GET'])
def login_result():
    return render_template('login-result.html')

# Movies CRUD
import route_movies

# Error Handling
import route_errors


if __name__ == '__main__':
    app.run()