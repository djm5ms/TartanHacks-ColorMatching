from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
from colorChecker import detect_colors



from SegCloth import segment_clothing

from PIL import Image

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
        if '.jpg' in filename:
            filename = filename.replace('.jpg', '.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        image = Image.open(filepath)

        result = segment_clothing(img=image, clothes = ["Upper-clothes"])
        
        
       
        result_filename = "result_" + filename
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        result.save(result_path)
        
        colors = detect_colors(result_path, num_colors=10)
       
   
        return render_template('index.html',
        message='File successfully uploaded',
        image=url_for('uploaded_file', filename=filename),
        image2=url_for('uploaded_file', filename=result_filename),
        colors=colors
        )

@app.route('/new-page')
def new_page():
    return '45'



if __name__ == '__main__':
    app.run(debug=True)
