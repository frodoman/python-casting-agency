import os
from casting_agency_app import app
from flask import Flask, render_template, request, abort, jsonify, session
from consts import *


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