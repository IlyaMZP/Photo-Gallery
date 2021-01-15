from flask import Flask, url_for, render_template, request, redirect, session
from sqlalchemy import desc

from flaskr import app, crawler
from flaskr.models import Picture, Album


@app.route('/', methods=['GET', 'POST'])
def index():
    album = request.args.get('album', None)
    if album and album != "0":
        return render_template('index.html', pictures=reversed(Picture.query.filter_by(album_id=album).all()), albums=reversed(Album.query.all()))
    else:
        return render_template('index.html', pictures=reversed(Picture.query.all()), albums=reversed(Album.query.all()))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('upload_images') + '?next=' + request.url)
    return response
