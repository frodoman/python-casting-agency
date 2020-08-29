import os
from flask import Flask, render_template, request, abort, jsonify, session
from consts import *
from flask_cors import CORS

def add_login_routes(app:Flask):

    @app.route('/login')
    def login():
        call_back = AUTH_CALL_BACK_DEV
        if KEY_AUTH_CALL_BACK in os.environ:
            call_back = os.environ[KEY_AUTH_CALL_BACK]

        return render_template('login.html', call_back_url=call_back)


    @app.route('/logout')
    def logout():
        session.clear()
        return render_template('login.html')


    @app.route('/login-result', methods=['GET'])
    def login_result():
        return render_template('login-result.html')


    return

def add_cors(app: Flask):
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request 
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    return 


def add_home_route(app:Flask):
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
    
    return