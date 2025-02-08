from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def renderImage():
    
    return render_template('index.html')

@app.route('/new-page')
def new_page():
    return '45'



if __name__ == '__main__':
    app.run(debug=True)
