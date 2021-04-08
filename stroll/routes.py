import os
import secrets
import sqlite3
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from stroll import app, db, bcrypt
from stroll.models import User, Journey
from flask_login import login_user, current_user, logout_user, login_required
from stroll.connect import get_all_users_json, get_user_json, get_all_user_journeys_json, get_one_user_journey_json, update_journey
from stroll.journeys import RadialJourney, SimpleJourney, getPolyline


# /users    GET: Shows list of users, POST: Add new user
# /users/user_id  GET: Just that user, PUT: Update user, DELETE
# /users/user_id/journeys   GET: List of journeys, POST: Create new journey
# /users/user_id/journeys/journey_id   PUT: Update journey, DELETE: Delete journey
# /login  POST
# /logout POST nothing
#! If have time: /users/username/.../?client_id=stuff&client_secret=stuff    for OAuth authentication
#! If have time: /users/username/attractions + /users/username/attractions/?attraction_id=stuff, otherwise just put in our own attractions
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/


@app.route("/", methods=['GET'])
def home():
    print("Person accessed website")
    return "<h1>Welcome to stroLL</h1>"


@app.route('/check_login_status')
def check_login_status():
    return str(current_user.is_authenticated)


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        content = get_all_users_json(json_str=True)
        return content
    elif request.method == "POST" and request.is_json:  # register new user
        content = request.get_json()
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
        return content


@app.route("/login", methods=['POST'])
def login():
    content = request.get_json()
    user = User.query.filter_by(username=content['username']).first()
    if not user or not bcrypt.check_password_hash(user.password, content['password']):
        return abort(403)
    login_user(user)
    return redirect('/')


@app.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return redirect('/')


@app.route("/users/<user_id>", methods=['GET'])
def userRequest(user_id):
    if request.method == 'GET':
        # if user has access, show everything, otherwise, show some stuff but don't show sensitive information like passwords
        content = get_user_json(user_id, json_str=True)
        return content


@app.route("/users/<user_id>/journeys", methods=['GET', 'POST'])
def journeys(user_id):
    if request.method == 'GET':
        # if user has access, show all journeys, if not, show only is_private = false journeys

        content = get_all_user_journeys_json(user_id, json_str=True)
        return content

    elif request.method == 'POST' and request.is_json:  # need to make error proof if malformed input passed
        content = request.get_json()
        # does user have access? if not 400 access denied
        """Expecting JSON in format:
        [
            journey_type: "Simple" or "Radial"
            origin: "[latitude (float), longitude (float)]"
            destination: "[latitude (float), longitude (float)]"
            [optional] waypoints: "[ [latitude (float), longitude (float)], [latitude (float), longitude (float)], ... ]"
            [optional] visit_nearby_attractions: "True" or "False"
            [optional, default 10] radius: kilometers (float)
        ]
        """
        #! Write an outer function or import for handling visit nearby attractions.
        journey_type = content['journey_type']
        origin, destination = content['origin'], content['destination']
        start_point_lat, start_point_long = content['origin'][
            'start_point_lat'], content['origin']['start_point_long']
        end_point_lat, end_point_long = content['destination'][
            'end_point_lat'], content['destination']['end_point_long']
        waypoints = content['waypoints'] or []
        gmapsOutput = None
        if journey_type == "Simple":
            journey = SimpleJourney(
                origin, destination, waypoints).getGmapsDirections()
            gmapsOutput = journey.getGmapsDirections()
        elif journey_type == "Radial":
            radius = content['radius'] or 10
            journey = RadialJourney(origin, destination, radius, waypoints, 5)
            gmapsOutput = journey.getGmapsDirections()
        else:
            return abort(404, "Unknown journey type")

        waypoints = journey.waypoints

        newJourney = Journey(
            user_id=user_id,
            start_point_long=start_point_long,
            start_point_lat=start_point_lat,
            end_point_long=end_point_long,
            end_point_lat=end_point_lat,
            waypoints=jsonify(waypoints),
            is_private=False,
            polyline=getPolyline(gmapsOutput)
        )
        db.session.add(newJourney)
        db.session.commit()
        return content


@app.route("/users/<user_id>/journeys/<journey_id>", methods=['PUT'])
def journeyRequest(user_id, journey_id):
    if request.method == 'PUT' and request.is_json:
        content = request.get_json()
        start_point_lat, start_point_long = content['origin'][
            'start_point_lat'], content['origin']['start_point_long']
        end_point_lat, end_point_long = content['destination'][
            'end_point_lat'], content['destination']['end_point_long']
        page_content = update_journey(start_point_lat, start_point_long, end_point_lat,
                                      end_point_long, content['waypoints'], content['journey_id'], json_str=True)
        # TODO: also update the polyline string, dont update journey_id, careful with waypoints as should be optional
        return page_content
