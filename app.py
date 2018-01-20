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

@app.route('/uploadalbum', methods=['POST'])
def upload_album():
    fileUrls = []
    albumId = uuid.uuid4().hex
    folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(folder):
        os.makedirs(folder)
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
        # check if the post request has the file part
        if 'files[]' not in request.files:
            return json.dumps({"ERROR":"Missing files[] object"}, indent=4)
        fileList = request.files.getlist('files[]')
        print(fileList)
        # if user does not select file, browser also
        # submit a empty part without filename
        for file in fileList:
            if file.filename == '':
                return json.dumps({"ERROR":"filename is blank"}, indent=4)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                directory = app.config['UPLOAD_FOLDER'] + '/' + albumId
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filePath = os.path.join(directory, filename)
                fileUrls.append(request.url_root + filePath)
                file.save(filePath)
        return json.dumps({"uploaded_photos":fileUrls}, indent=4)

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
