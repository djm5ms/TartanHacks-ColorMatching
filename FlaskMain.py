from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

from SegCloth import segment_clothing

#function for removing the background of clothes
def segment(img, clothes):
    return segment_clothing(img, clothes)


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if 'imageUpload' not in request.files:
        return 'No file part'
    file = request.files['imageUpload']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

@app.route('/new-page')
def new_page():
    return '45'



if __name__ == '__main__':
    app.run(debug=True)
