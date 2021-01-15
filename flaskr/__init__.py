from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import click
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_pyfile('app.cfg')
app.permanent_session_lifetime = timedelta(minutes=10)

db = SQLAlchemy(app)

from flaskr import models, routes, crawler, admin_routes
from flaskr.models import User

db.create_all()
crawler.update_db()

admin = User.query.first()
if admin is None:
    hash_pwd = generate_password_hash(app.config['ADMIN_PASSWORD'])
    new_user = User(username=app.config['ADMIN_USERNAME'], password=hash_pwd)
    db.session.add(new_user)
    db.session.commit()

def create_app():
    return app

