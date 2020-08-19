import os
from flask import Flask, render_template, request, abort, jsonify
from models import db, set_up_db
from flask_migrate import Migrate
from flask_cors import CORS

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
def get_greeting():
    debug = False
    if app.debug:
        debug = True

    return jsonify({
        "Index": "Home", 
        "Debug": debug,
        "Database": app.config['SQLALCHEMY_DATABASE_URI']
    })

if __name__ == '__main__':
    app.run()