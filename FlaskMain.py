from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User 

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

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'user-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')



db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('hello'))
        
        return 'Invalid credentials'
    
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            return 'Username already exists'

        new_user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))




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
    with app.app_context():
        db.create_all()
    if current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('login'))
    


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
        clothes=clothes
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
    print(f"Looking for clothing with name: {name}")  # Debug print
    
    for clothing in clothes:
        print(f"Checking clothing: {clothing.getImg()}")  # Debug print
        if clothing.getImg() == name:
            result_dict = possibleClosestCompliment(clothes, clothing)
            print(f"Result dictionary: {result_dict}")  # Debug print
            print(f"Result keys: {result_dict.keys()}")  # Debug print
            
            return render_template('bestMatch.html', 
                                 clothes=clothes, 
                                 dictcomp=result_dict, 
                                 dictcont=result_dict)
    
    return "Clothing item not found", 404



    
    




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


