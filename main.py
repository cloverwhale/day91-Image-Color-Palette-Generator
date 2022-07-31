import os
from datetime import datetime as dt
from PIL import UnidentifiedImageError
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from imagefile import ImageFile
from colorpalette import ColorPalette
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)
scheduler = BackgroundScheduler()
scheduler.start()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_file(filepath):
    os.remove(filepath)
    print(filepath)
    return scheduler.remove_job(filepath)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            current_time = dt.now().strftime('%Y_%m_%d_%H%M%S')
            filename = secure_filename(file.filename)
            filename_final = f"{current_time}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_final))
            return redirect(url_for('results', name=filename_final))

    return render_template('index.html')


@app.route("/results/<name>")
def results(name):
    img_file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    scheduler.add_job(lambda: delete_file(img_file_path), 'interval', minutes=1, id=img_file_path)

    try:
        img = ImageFile(img_file_path)
    except UnidentifiedImageError:
        flash('Cannot identify image file')
        return redirect(url_for('index'))

    color_palette = ColorPalette(img.resized_img_arr_list())
    hex_color = color_palette.get_major_color()[1]
    img_url = f".{img_file_path}"

    return render_template('results.html', img_url=img_url, hex_color=hex_color)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5301, debug=True)
