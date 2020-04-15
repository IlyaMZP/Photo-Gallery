from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr import app, db, crawler
from flaskr.models import User, Picture


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html', pictures=Picture.query.all())
    else:
        username = session.get('logged_in')
        if request.method == 'POST':
            return render_template('index.html', name=username , data=123)
        return render_template('index.html', name=username)


@app.route('/update_db')
def update_database():
    crawler.update_db()
    return "Ok"


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        crawler.update_db()
        return render_template('login.html')
    else:
        login = request.form['username']
        passw = request.form['password']
        if login and passw:
            try:
                user = User.query.filter_by(username=login).first()
                if user and check_password_hash(user.password, passw):
                    session['logged_in'] = login
                    return redirect(url_for('home'))
                else:
                    return 'Wrong username or password'
            except:
                return "User not found"
        else:
            return "Missing username or password"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        login=request.form['username']
        passw=request.form['password']
        if login and passw:
            try:
                hash_pwd = generate_password_hash(passw)
                new_user = User(username=login, password=hash_pwd)
                db.session.add(new_user)
                db.session.commit()
                return render_template('login.html')
            except:
                return render_template('register.html', error="User exists")
        else:
            return render_template('register.html', error="Missing login or password")


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)

    return response
