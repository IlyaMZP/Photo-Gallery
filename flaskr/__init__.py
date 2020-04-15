from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
app.permanent_session_lifetime = timedelta(minutes=10)

db = SQLAlchemy(app)

from flaskr import models, routes, crawler

db.create_all()
crawler.update_db()

def create_app():
    return app
