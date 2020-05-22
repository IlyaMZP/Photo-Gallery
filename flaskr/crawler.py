from os import walk, path, remove, chdir, getcwd
from hashlib import md5
from PIL import Image
import re

from flaskr import db, app
from flaskr.models import Picture


images_path = 'static/gallery/'
thumbnails_path = 'static/thumbnails/'
error_thumbnail = 'static/thumbnails/error.jpg'

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def image_list():
    files = []
    for r, d, f in walk(images_path):
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
    images = image_list()
    for picture in Picture.query.all():
        if picture.image not in images:
            try:
                remove(picture.thumbnail)
            except:
                pass
            db.session.delete(picture)
            db.session.commit()
    for filename in images:
        image = Picture.query.filter_by(image=filename).first()
        if not image:
            thumbnail = gen_thumbnail(filename)
            new_image = Picture(filename, thumbnail)
            db.session.add(new_image)
            db.session.commit()
    chdir(current_wd)
    print("Database Updated")

