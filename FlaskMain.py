from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
from colorChecker import detect_colors
import numpy as np


class clothingItem(object):
    def __init__(self, img, type, colors=[], percemnts=[], name=""):
        self.name = name
        self.img = img
        self.type = type
        self.colors = colors
        self.percemnts = percemnts
    def getImg(self):
        return self.img
    def getType(self):
        return self.type
    def getColors(self):
        return self.colors
    def getPercemnts(self):
        return self.percemnts
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def setImg(self, img):
        self.img = img
    def setType(self, type):
        self.type = type
    def setColors(self, colors):
        self.colors = colors
    def setPercemnts(self, percemnts):
        self.percemnts = percemnts
        
clothes=[]
updatedPaths=[]

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
        checking=request.form['clothingType']

<<<<<<< HEAD
        result = segment_clothing(img=image, clothes=checking)
=======
        try:
            result = segment_clothing(img=image, clothes=[checking])
        except:
            result = segment_clothing(img=image)
>>>>>>> 55d2a3b0a467b8d79dcf9a5ccffe269c725e180a
        
        
        
       
        result_filename = "result_" + filename
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        result.save(result_path)
        
        adjusted_path=url_for('uploaded_file', filename=result_filename)
        
        
        
        
        colors, percents = detect_colors(result_path, num_colors=10)
        if adjusted_path not in updatedPaths:
            clothes.append(clothingItem(adjusted_path, "Upper-clothes", colors, percents))
        updatedPaths.append(adjusted_path)
        return render_template('index.html',
        message='File successfully uploaded',
        image=url_for('uploaded_file', filename=filename),
        image2=url_for('uploaded_file', filename=result_filename),
        colors=colors,
        percents=percents,
        clothes=clothes,
        checking=type(checking)
        )

@app.route('/new-page')
def new_page():
    return render_template('new_page.html',
        clothes=clothes)



if __name__ == '__main__':
    app.run(debug=True)
