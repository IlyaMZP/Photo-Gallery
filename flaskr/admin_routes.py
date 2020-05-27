from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from os import path, remove

from flaskr import app, db, crawler
from flaskr.models import User, Picture


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/admin/upload_images', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'GET':
        if session.get('logged_in'):
            username = session.get('logged_in')
            return render_template('admin/upload_images.html', username=username)
        else:
            return render_template('admin/login.html')
    else:
        if request.files and session.get('logged_in'):
            images = request.files.getlist("image[]")
            for image in images:
                if image.filename == "":
                    print("No filename")
                    return redirect(url_for('upload_images'))
                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(path.join(app.config["IMAGE_UPLOADS"], filename))
            return redirect(url_for('upload_images'))


@app.route('/login', methods=['POST'])
def login():
    login = request.form['username']
    passw = request.form['password']
    if login and passw:
        try:
            user = User.query.filter_by(username=login).first()
            if user and check_password_hash(user.password, passw):
                session['logged_in'] = login
                return redirect(url_for('upload_images'))
            else:
                return 'Wrong username or password'
        except:
            return "User not found"
    else:
        return "Missing username or password"


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/admin/delete_images', methods=['GET', 'POST'])
def delete_images():
    if session.get('logged_in'):
        if request.method == 'GET':
            username = session.get('logged_in')
            return render_template('admin/delete_images.html', pictures=Picture.query.all(), username=username)
        else:
            image_id = request.form['id']
            if image_id:
                picture = Picture.query.filter_by(id=image_id).first()
                remove(path.join(app.root_path, picture.image))
                remove(path.join(app.root_path, picture.thumbnail))
                db.session.delete(picture)
                db.session.commit()
                return "Ok"
            else:
                return render_template('admin/delete_images.html', pictures=Picture.query.all(), username=username), 401
    else:
        return redirect(url_for('upload_images'))


@app.route('/admin/update_db')
def update_database():
    if session.get('logged_in'):
        crawler.update_db()
        return redirect(url_for('upload_images'))
    else:
        return "Error"


@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    if app.config['ALLOW_REGISTRATION'] == 'True':
        if request.method == 'GET':
            return render_template('admin/register.html')
        else:
            login=request.form['username']
            passw=request.form['password']
            if login and passw:
                try:
                    hash_pwd = generate_password_hash(passw)
                    new_user = User(username=login, password=hash_pwd)
                    db.session.add(new_user)
                    db.session.commit()
                    return render_template('admin/login.html')
                except:
                    return render_template('admin/register.html', error="User exists")
            else:
                return render_template('admin/register.html', error="Missing login or password")
    else:
        return render_template('admin/register.html', error="Registration disabled")


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response
