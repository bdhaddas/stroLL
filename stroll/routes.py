import os
import secrets
from flask import render_template, url_for, flash, redirect, request, jsonify
from stroll import app, db, bcrypt
from stroll.forms import RegisterForm, LoginForm, UpdateForm, MapForm, PreferencesForm
from stroll.models import User
from flask_login import login_user, current_user, logout_user, login_required
from stroll.journeys.journeyMaker import coord_radial, get_directions


journeys = [
    {
        'author': 'User1',
        'title': 'My Afternoon Walk',
        'content': 'Map route, text field',
        'date_posted': 'April 2, 2021'
    },
    {
        'author': 'User2',
        'title': 'My Morning Walk',
        'content': 'Map route, text field',
        'date_posted': 'April 3, 2021'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', journeys=journeys)


@app.route("/control", methods=['GET', 'POST'])
def control():
    form = MapForm()
    return render_template('control.html', title='API Control', form=form)


@app.route("/directions", methods=['GET', 'POST'])
def getdirections():
    # TODO: Use newer / non-deprecated methods within POST
    if request.method == "POST":

        user_lat_long = request.form['origin_lat_long']
        user_direction = request.form['direction']

        user_lat_long = user_lat_long.split(",")
        user_lat_long = list(map(float, user_lat_long))

        waypoints = coord_radial(
            user_lat_long, 1, user_direction)  # ! Deprecated
        routecycle = get_directions(
            user_lat_long, user_lat_long, waypoints)  # ! Deprecated

        return jsonify(routecycle)

    return redirect("/control")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                           form=form)


@app.route("/preferences_set", methods=['POST'])  # <id>
@login_required
def preferences():
    form = PreferencesForm()
    if form.validate_on_submit():
        current_user.water = form.water.data
        current_user.green_spaces = form.green_spaces.data
        current_user.traffic = form.traffic.data
        current_user.buildings = form.buildings.data
        current_user.pace = form.pace.data
        db.session.commit
        flash('Preferences successfully set', 'success')
        # return redirect(url_for('account/preferences'))
    return render_template('preferences_set.html', title='Set Pref', form=form)

# @app.route("/preferences", methods=['GET'])
# @login_required
    # return render_template('preferences.html', title='preferences')


@app.route("/preferences_update", methods=['PUT'])
@login_required
def updatePreferences():
    form = PreferencesForm()
    if form.validate_on_submit():
        current_user.water = form.water.data
        current_user.green_spaces = form.green_spaces.data
        current_user.traffic = form.traffic.data
        current_user.buildings = form.buildings.data
        current_user.pace = form.pace.data
        db.session.commit
        flash('Preferences successfully updated', 'success')
        # return redirect(url_for('account/preferences'))
    return render_template('preferences_update.html', title='Update Pref', form=form)
