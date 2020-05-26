from flask import Flask, url_for, render_template, request, redirect, session

from flaskr import app
from flaskr.models import Picture


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('logged_in'):
        username = session.get('logged_in')
        return render_template('index.html', pictures=reversed(Picture.query.all()), username=username)
    else:
        return render_template('index.html', pictures=reversed(Picture.query.all()))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('upload_images') + '?next=' + request.url)
    return response
