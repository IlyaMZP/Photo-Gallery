from flaskr import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Picture(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(), unique=True)
    thumbnail = db.Column(db.String(), unique=True)

    def __init__(self, image, thumbnail):
        self.image = image
        self.thumbnail = thumbnail
