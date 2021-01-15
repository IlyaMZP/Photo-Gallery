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
    thumbnail = db.Column(db.String())
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    def __init__(self, image, thumbnail, album_id):
        self.image = image
        self.thumbnail = thumbnail
        self.album_id = album_id

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    pictures = db.relationship("Picture", cascade="all, delete-orphan", backref="images")
    album_name = db.Column(db.String(255), unique=True)
    thumbnail = db.Column(db.String(255), unique=True)

    def __init__(self, album_name, thumbnail):
        self.album_name = album_name
        self.thumbnail = thumbnail
