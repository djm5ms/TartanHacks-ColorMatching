from flask import Flask, render_template, request, url_for
from PIL import Image
import os
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
from SegCloth import segment_clothing


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_FOLDER_URL'] = '/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


    

# Serve the uploads folder as a static folder
app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': app.config['UPLOAD_FOLDER']
})


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
        seg_file=segment_clothing(Image.open(f'uploads/{filename}'))
        seg_filename='checker'+secure_filename(seg_file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        seg_file.save(os.path.join(app.config['UPLOAD_FOLDER'], seg_filename))
        
        return render_template('index.html',
        message='File successfully uploaded',
        image=url_for('uploaded_file', filename=filename),
        image2=url_for('uploaded_file', filename=seg_filename)  
        )

@app.route('/new-page')
def new_page():
    return '45'



if __name__ == '__main__':
    app.run(debug=True)
