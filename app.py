import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import imghdr
from PIL import Image

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        file_in = './uploads/' + filename
        # compress_PIL(file_in, 1)
        # file_out = get_outfile(filename)
        # file_out = './uploads/' + file_out
        return render_template('upload.html', file_in=file_in, file_out=file_out)


# @app.route('/upload/compress', methods=['POST'])
# def compress():
#         compress_PIL(file_in, 1)
#         file_out = get_outfile(filename)
#         file_out = './uploads/' + file_out
#     return render_template('upload.html', file_in=file_in, file_out=file_out)


def get_outfile(infile):
    baseName, e = os.path.splitext(infile)
    f, e = os.path.splitext(infile)
    f = (baseName + str("_compress"))
    outfile = f + ".jpg"
    return outfile


# File compressing by compress_PIL(path_file, 1)
def compress_PIL(infile, times):
    baseName, e = os.path.splitext(infile)
    try:
        f, e = os.path.splitext(infile)
        f = (baseName + str("_compress"))
        outfile = f + ".jpg"
        #open previously generated file
        compImg = Image.open(infile)
        #compress file at 50% of previous quality
        compImg.save(outfile, "JPEG", quality=20)
    except IOError:
        print("Cannot convert", infile)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8080"),
        debug=True
    )
