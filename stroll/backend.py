import os
import secrets
import sqlite3
from flask import render_template, url_for, flash, redirect, request, jsonify
from stroll import app, db, bcrypt
from stroll.forms import RegisterForm, LoginForm, UpdateForm, MapForm, PreferencesForm
from stroll.models import User, Journey
from flask_login import login_user, current_user, logout_user, login_required
from stroll.journeys import RadialJourney, SimpleJourney, attractionFinder
from stroll.connect import get_all_users_json, get_user_json, get_all_user_journeys, get_one_user_journey, db

# /users    GET: Shows list of users, POST: Add new user
# /users/username   GET: Just that user, PUT: Update user
# /users/username/journeys   GET: List of journeys, POST: Create new journey
# /users/username/journeys/?journey_id=stuff    GET: Just the journey, PUT: Update journey
# forgot also, DELETE for journey_id
#! If have time: /users/username/.../?client_id=stuff&client_secret=stuff    for OAuth authentication
#! If have time: /users/username/attractions + /users/username/attractions/?attraction_id=stuff, otherwise just put in our own attractions
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/


@app.route("/", methods=['GET'])
def home():
    print("Person accessed website")
    return "<h1>Welcome to stroLL</h1>"


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        return get_all_users_json(json_str=True)
        # pull data from database of all users (without revealing password / sensitive info) and put into a JSON to return via jsonify()
    elif request.method == "POST" and request.is_json:
        content = request.get_json()
        """Expected:
        {
            username: str
            email: str
            password: str
            [optional]water: bo
        username = request.args.get('username')ol
        content =     [optional]green_spaces: bool

        return content            [optional]buildings: bool
            [optional]pace: integer (kilometers per hour)
        }
        """
        print(content)
        # if user doesn't already exist: (not sure how to check this)
        hashed_password = bcrypt.generate_password_hash(
            content['password']).decode('utf-8')
        user = User(username=content['username'],
                    email=content['email'],
                    password=hashed_password,
                    water=content['water'] or False,
                    green_spaces=content['green_spaces'] or False,
                    buildings=content['buildings'] or False,
                    pace=content['pace'] or 7
                    )
        db.session.add(user)
        db.session.commit()


@app.route("/users/<username>", methods=['GET', 'PUT'])
def userRequest(username):
    if rcontent = equest.method == 'GET':
        get_user_json(username, json_str=True)
    elif request.method == 'PUT' and request.is_json:
        content = request.get_json()
        print(content)


@app.route("/users/username/journeys", methods=['GET', 'POST'])
def journeys():
    if request.method == 'GET':
        get_all_user_journeys_json(user_id, json_str=True)
    elif request.method == 'POST' and request.is_json:
        content = request.get_json()
        print(content)


@app.route("/users/username/journeys/?journey_id=stuff", methods=['GET', 'PUT'])
def journeyRequest():
    if request.method == 'GET':
        get_one_user_journey_json(user_id, id, json_str=True)
    elif request.method == 'PUT' and request.is_json:
        content = request.get_json()
        print(content)
