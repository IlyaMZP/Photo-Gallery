from flask import Flask, url_for, render_template, request, redirect, session

from flaskr import app
from flaskr.models import Picture


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('logged_in'):
        username = session.get('logged_in')
        return render_template('index.html', pictures=Picture.query.all(), username=username)
    else:
        return render_template('index.html', pictures=Picture.query.all())


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response
