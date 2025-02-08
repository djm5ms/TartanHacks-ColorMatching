from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
from colorChecker import detect_colors
import numpy as np
from complementary import *
from SegCloth import segment_clothing
from PIL import Image



clothes=[]
updatedPaths=[]

from SegCloth import segment_clothing

from PIL import Image



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_FOLDER_URL'] = '/uploads'

imgDir=app.config['UPLOAD_FOLDER_URL']

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



        try:
            result = segment_clothing(img=image, clothes=[checking])
        except:
            result = segment_clothing(img=image)

        
        
        
       
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
        
        )

@app.route('/new-page')
def new_page():
    return render_template('new_page.html',
        clothes=clothes,
        imgDir=imgDir)


@app.route('/new-page', methods=['POST'])
def rgbList():
    compliments = makeRGBCompliments(clothes)
    closestMatch = closestCompliment(clothes[0], compliments, clothes)
    return f"Closest compliment to {clothes[0].name} is {closestMatch.name}"

        
    
    

@app.route('/item/<string:name>')
def item_view(name):
    name= f"{app.config['UPLOAD_FOLDER_URL']}/{name}"
    
    for clothing in clothes:
        if clothing.getImg() == name:
            return render_template('itemView.html', clothing=clothing, imgDir=imgDir)
    return "Not Found"    

@app.route('/goodMatch/<string:name>')
def goodMatch(name):
    name = f"{app.config['UPLOAD_FOLDER_URL']}/{name}"
    clothing2 = None
    for clothing in clothes:
        if clothing.getImg() == name:
            clothing2 = clothing
            break  # Use break instead of exit
    
    if clothing2 is None:
        return "Clothing item not found", 404  # Return an error if no match is found
    
    dict = possibleClosestCompliment(clothes, clothing2)
    return render_template('bestMatch.html', clothes=clothes, dictcomp=dict, dictcont=dict)




if __name__ == '__main__':
    app.run(debug=True)


