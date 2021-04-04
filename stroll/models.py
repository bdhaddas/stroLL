from datetime import datetime
from stroll import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # journey = db.relationship('Journey', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    journey_image_file = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_point = db.Column(db.Integer, nullable=False)
    end_point = db.Column(db.Integer, nullable=False)
    length_distance = db.Column(db.Integer, nullable=False) #may change to float

    def __repr__(self):
        return f"Journey('{self.name}', '{self.date_posted}')"

class Attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    attractionName = db.Column(db.String(100), nullable=False)
    attractionDescriptor = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Attraction('{self.attractionName}', '{self.attractionDescriptor}', ('{self.latitude}','{self.longitude}')"
