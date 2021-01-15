from os import walk, path, remove, chdir, getcwd, listdir
from hashlib import md5
from PIL import Image
import re

from flaskr import db, app
from flaskr.models import Picture, Album


images_path = 'static/gallery/'
thumbnails_path = 'static/thumbnails/'
error_thumbnail = 'static/thumbnails/error.jpg'

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def dir_list():
    return sorted(listdir(images_path), key=natural_keys)


def image_list(dirs):
    files = []
    for directory in dirs:
        for r, d, f in walk(path.join(images_path, directory)):
            for file in sorted(f, key=natural_keys):
                if '.jpg' or '.jpeg' or '.png' or '.webp' in file:
                    files.append(path.join(r, file))
    return files

def gen_md5(filename):
    hash_md5 = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def gen_thumbnail(image):
    md5sum = gen_md5(image)
    thumbnail = path.join(thumbnails_path, md5sum + ".jpg")
    try:
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        rgb_im.thumbnail((128 , 128), Image.ANTIALIAS)
        rgb_im.save(thumbnail, "JPEG")
    except IOError:
        print("Can't create thumbnail for", image)
        return error_thumbnail
    return thumbnail

def update_db():
    current_wd = getcwd()
    chdir(app.root_path)
    dirs = dir_list()
    images = image_list(dirs)
    for picture in Picture.query.all():
        if picture.image not in images:
            try:
                remove(picture.thumbnail)
            except:
                pass
            db.session.delete(picture)
            db.session.commit()
    for album in Album.query.all():
        if album.album_name not in dirs:
            print(dirs)
            print(album.album_name)
            db.session.delete(album)
            db.session.commit()
    for filename in images:
        image = Picture.query.filter_by(image=filename).first()
        if not image:
            thumbnail = gen_thumbnail(filename)
            im_path = path.dirname(filename)
            album_name = path.basename(im_path)
            album = Album.query.filter_by(album_name=album_name).first()
            if not album:
                album = Album(album_name, thumbnail)
                db.session.add(album)
                db.session.commit()
            else:
                album = Album.query.filter_by(album_name=album_name).one()
            new_image = Picture(filename, thumbnail, album.id)
            db.session.add(new_image)
            db.session.commit()
    chdir(current_wd)
    print("Database Updated")

