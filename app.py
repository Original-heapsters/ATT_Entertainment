import json
import os
import shutil
import uuid
import ImageRecog
from flask import Flask, request, flash, url_for, redirect, render_template, abort, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
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

@app.route('/uploadalbum', methods=['POST'])
def upload_album():
    fileUrls = []
    albumId = uuid.uuid4().hex
    folder = app.config['UPLOAD_FOLDER']
    for the_file in os.listdir(folder):
        print(the_file)
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files[]' not in request.files:
            return "Missing file"
        fileList = request.files.getlist('files[]')
        print(fileList)
        # if user does not select file, browser also
        # submit a empty part without filename
        for file in fileList:
            if file.filename == '':
                return "Filename is blank"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                directory = app.config['UPLOAD_FOLDER'] + '/' + albumId
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filePath = os.path.join(directory, filename)
                fileUrls.append(request.url_root + filePath)
                file.save(filePath)
        return json.dumps(fileUrls, indent=4)
    return

    return json.dumps(sample, indent=4, sort_keys=True)

@app.route('/analyze')
def analyze():
    recog = ImageRecog.ImageRecog()
    finalPrediction = recog.analyzeImage()
    print(json.dumps(finalPrediction, indent=4, sort_keys=True))
    return json.dumps(finalPrediction, indent=4, sort_keys=True)




## AUX methods
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
