from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import func
from os import path, mkdir, remove
from shutil import rmtree

from flaskr import app, db, crawler
from flaskr.models import User, Picture, Album


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/upload_images', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'GET':
        if session.get('logged_in'):
            username = session.get('logged_in')
            return render_template('admin/upload_images.html', username=username, albums=Album.query.all())
        else:
            return render_template('admin/login.html')
    else:
        if request.files and session.get('logged_in'):
            album_id = request.form['album_id']
            album_name = request.form['album_name']
            for key, f in request.files.items():
                if key.startswith('file'):
                    if f == "":
                        print("No filename")
                        return redirect(url_for('upload_images'))
                    if allowed_image(f.filename):
                        filename = secure_filename(f.filename)
                        if album_id != "0":
                            album_dir = Album.query.filter_by(id=album_id).first().album_name
                        else:
                            album_dir = str(db.session.query(Album).count() + 1) + "_"
                            album_dir += album_name
                            try:
                                mkdir(path.join(app.config["IMAGE_UPLOADS"], album_dir))
                            except FileExistsError:
                                pass
                        f.save(path.join(app.config["IMAGE_UPLOADS"], album_dir, filename))
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


@app.route('/delete_images', methods=['GET', 'POST'])
def delete_images():
    if session.get('logged_in'):
        if request.method == 'GET':
            username = session.get('logged_in')
            album_id = request.args.get('album_id', None)
            if album_id and album_id != "0":
                album_dir = Album.query.filter_by(id=album_id).first().album_name
                try:
                    rmtree(path.join(app.config["IMAGE_UPLOADS"], album_dir))
                except:
                    pass
                Album.query.filter_by(id=album_id).delete()
                db.session.commit()
            return render_template('admin/delete_images.html', pictures=Picture.query.all(), username=username, albums=Album.query.all())
        else:
            image_id = request.form['image_id']
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


@app.route('/update_db')
def update_database():
    if session.get('logged_in'):
        crawler.update_db()
        return redirect(url_for('upload_images'))
    else:
        return "Error"


@app.route('/register', methods=['GET', 'POST'])
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
