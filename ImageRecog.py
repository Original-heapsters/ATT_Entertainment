import os
import json
import config
import random
import subprocess
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

class ImageRecog:

    def __init__(self, imageDir):
        self.app = ClarifaiApp(api_key=config.conf['clarify_key'])
        self.model = self.app.models.get("general-v1.3")
        self.imageDir = imageDir
        self.clarifaiData = {}

    def analyzeImages(self):
        imageArray = []
        for the_file in os.listdir(self.imageDir):
            print(the_file)
            image = ClImage(file_obj=open(os.path.join(self.imageDir, the_file), 'rb'))
            imageArray.append(image)
        response = self.model.predict(imageArray)
        self.clarifaiData  = response
        self.digestData()
        return response

    def createVideo(self):
        category = 'adventure'
        path, dirs, files = os.walk(self.imageDir).next()
        clip_count = len(files)

        if not os.path.exists('./static/music/' + category + '/short/'):
            os.makedirs('./static/music/' + category + '/short/')

        musicDir = './static/music/'+ category
        audioShortenCommand = 'ffmpeg -y -t 3 -i '
        currentTime = 0.0
        path, dirs, files = os.walk('./static/music/'+ category).next()
        musicFileCount = len(files)
        inputArray = []
        complexFilter = ""
        for count in range(0,clip_count):
            # Choose random music file
            musicFile = files[random.randint(0,musicFileCount-1)]
            fullCommand = audioShortenCommand + './static/music/'+ category + '/' + musicFile + ' ./static/music/'+category + '/short/' + musicFile
            p = subprocess.Popen(fullCommand, stdout=subprocess.PIPE, shell=True)
            p.communicate()
            p.wait()
            inputArray.append('-i ./static/music/'+ category + '/short/' + musicFile + ' ')
            complexFilter += '[' + str(count) + ':0]'
            currentTime += 0.3
        muxCommand = "ffmpeg -y "
        # muxCommand = "ffmpeg -i heavenShort.mp3 -i alexShort.mp3 -filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' -map '[out]' muxed.mp3"
        currentTime = 0.0
        for count in range(0,clip_count):
            muxCommand += inputArray[count]
            # Choose random music file
        muxCommand += " -filter_complex '" + complexFilter + "concat=n=" + str(clip_count) + ":v=0:a=1[out]' -map '[out]' ./static/music/"+ category + "/muxed.mp3"

        print(muxCommand)
        p = subprocess.Popen(muxCommand, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()

        videoGenCommand = 'ffmpeg -y -r 1/3 -i ' + self.imageDir + '/image_%04d.png ' + self.imageDir + '/out.mp4'
        p = subprocess.Popen(videoGenCommand, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()

        combineCommand = "ffmpeg -y -i " + self.imageDir + "/out.mp4 -i ./static/music/" + category + "/muxed.mp3 -c copy " + self.imageDir + "/combined.mp4"
        p = subprocess.Popen(combineCommand, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()

        os.remove(os.path.join(self.imageDir, "out.mp4") )
        jsonFile = os.path.join(self.imageDir, "imageAnalysis.json")
        with open(jsonFile, 'w') as outfile:
            json.dump(self.clarifaiData, outfile)


    def digestData(self):
        print(json.dumps(self.clarifaiData))
        print("digest")

    def findEmotion(self):
        print("finding emotion")

    def findTheme(self):
        print("Finding theme")

    def findProduct(self):
        print("Finding product")
