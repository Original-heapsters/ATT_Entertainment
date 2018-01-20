import json
from flask import Flask, request, flash, url_for, redirect, render_template, abort, send_from_directory

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    indexObj = {"one":"two"}
    return json.dumps(indexObj)

@app.route('/upload')
def upload():
    sample = {'ObjectInterpolator': 1629,  'PointInterpolator': 1675, 'RectangleInterpolator': 2042}

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "Missing file"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "Filename is blank"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File upload success"
    return

    return json.dumps(sample)
@app.route('/analyze')
def analyze():
    return "Yo dawg, I heard you like testing endpoints so i put and endpoint in your endpoint"


## AUX methods
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
  app.run(host:'0.0.0.0', port=5000, debug=True)
