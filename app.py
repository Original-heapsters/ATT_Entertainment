import json
import os
import glob2
import shutil
import uuid
import ImageRecog
from flask_cors import CORS
from flask import Flask, request, flash, url_for, redirect, render_template, abort, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

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
            return json.dumps({"ERROR":e})
    # check if the post request has the file part
    if 'files[]' not in request.files:
        return json.dumps({"ERROR":"Missing files[] object"}, indent=4)
    fileList = request.files.getlist('files[]')
    print(fileList)
    # if user does not select file, browser also
    # submit a empty part without filename
    fileCount = 0
    for file in fileList:
        if file.filename == '':
            return json.dumps({"ERROR":"filename is blank"}, indent=4)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            directory = app.config['UPLOAD_FOLDER'] + '/' + albumId
            if not os.path.exists(directory):
                os.makedirs(directory)
            filePath = os.path.join(directory, 'image_{:04d}'.format(fileCount) + file.filename[filename.rfind('.'):])
            fileUrls.append(request.url_root + filePath)
            file.save(filePath)
            fileCount += 1
    finalTagList = analyze(directory)
    # videoPath = os.path.join(directory,"out.mp4")
    # finalTagList["videoURL"] = videoPath
    # response = {"videoURL":request.url_root + videoPath, "ClarifaiData" : finalTagList}
    # return json.dumps(response, indent=4)
    return finalTagList

@app.route('/previewAnalysis')
def preview_analysis():

    for filename in glob2.glob(os.path.join(app.config['UPLOAD_FOLDER'], '**/*.json')):
        print(filename)
        try:
            return json.dumps(json.load(open(filename)))
        except ValueError:
            return json.dumps({"ERROR":"No json data found"})
    return json.dumps({"ERROR":"No json data found"})


@app.route('/getvideo')
def get_video():
    for filename in glob2.glob(os.path.join(app.config['UPLOAD_FOLDER'], '**/*.mp4')):
        print(filename)
        # filePath = os.path.join(directory, 'image_{:04d}'.format(fileCount) + file.filename[filename.rfind('.'):])
        outputURL = request.url_root + filename
        return json.dumps({"VideoURL":outputURL})

    return json.dumps({"ERROR":"No video found"})

def analyze(imagesDir):
    recog = ImageRecog.ImageRecog(imageDir=imagesDir)
    finalPrediction = recog.analyzeImages()
    return json.dumps(finalPrediction, indent=4, sort_keys=True)




## AUX methods
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
