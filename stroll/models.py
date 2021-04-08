from datetime import datetime
from stroll import app, db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    water = db.Column(db.Boolean)
    green_spaces = db.Column(db.Boolean)
    traffic = db.Column(db.Boolean)
    buildings = db.Column(db.Boolean)
    pace = db.Column(db.Integer)
    # journey = db.relationship('Journey', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    journey_image_file = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_point_long = db.Column(db.Integer, nullable=False)
    start_point_lat = db.Column(db.Integer, nullable=False)
    end_point_long = db.Column(db.Integer, nullable=False)
    end_point_lat = db.Column(db.Integer, nullable=False)
    length_distance = db.Column(
        db.Integer, nullable=False)  # may change to float

    def __repr__(self):
        return f"Journey('{self.name}', '{self.date_posted}')"


class Attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attr_lat = db.Column(db.String, nullable=False)
    attr_long = db.Column(db.String, nullable=False)
    attractionName = db.Column(db.String(100), nullable=False)
    attractionDescriptor = db.Column(db.String(100), nullable=False)
    water = db.Column(db.Boolean, nullable=False)
    green_spaces = db.Column(db.Boolean, nullable=False)
    traffic = db.Column(db.Boolean, nullable=False)
    buildings = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Attraction('{self.attractionName}', '{self.attractionDescriptor}', ('{self.latitude}','{self.longitude}')"
