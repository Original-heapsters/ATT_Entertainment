import os
import json
import glob2
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
        self.logoModel = self.app.models.get("logo")
        self.imageDir = imageDir
        self.clarifaiData = {}
        self.logoData = {}
        self.imageMeta = {}

    def analyzeImages(self):
        imageArray = []
        for the_file in sorted(os.listdir(self.imageDir)):
            print(the_file)
            image = ClImage(file_obj=open(os.path.join(self.imageDir, the_file), 'rb'))
            imageArray.append(image)
        response = self.model.predict(imageArray)
        logoResponse = self.logoModel.predict(imageArray)
        self.clarifaiData  = response
        self.logoData = logoResponse
        self.digestData()
        return response

    def createVideo(self):
        path, dirs, files = os.walk(self.imageDir).next()
        clip_count = len(files)
        images = glob2.glob(os.path.join(self.imageDir, '**/*.png'))
        audioShortenCommand = 'ffmpeg -y -t 3 -i '
        muxCommand = "ffmpeg -y "
        complexFilter = ""
        currentClip = 0
        timingLines = []
        timingFile = open(self.imageDir + '/timing.ffconcat', 'w')
        timingFile.write("ffconcat version 1.0\n")
        for count in range(0,clip_count-1):
            print(self.imageMeta)
            print(int(count))
            category = self.imageMeta[int(count)]["emotion"]
            path, dirs, musicfiles = os.walk('./static/music/'+ category).next()
            musicFileCount = len(musicfiles)
            musicDir = './static/music/'+ category
            if not os.path.exists('./static/music/' + category + '/short/'):
                os.makedirs('./static/music/' + category + '/short/')
            # Choose random music file
            musicFile = musicfiles[random.randint(0,musicFileCount-1)]
            fullCommand = audioShortenCommand + './static/music/'+ category + '/' + musicFile + ' ./static/music/'+category + '/short/' + musicFile
            p = subprocess.Popen(fullCommand, stdout=subprocess.PIPE, shell=True)
            p.communicate()
            p.wait()
            muxCommand += '-i ./static/music/'+ category + '/short/' + musicFile + ' '
            complexFilter += '[' + str(count) + ':0]'
            timingLines.append("file image000" + str(currentClip) + ".png \nduration 3 \n")
            currentClip += 1

        for line in timingLines:
            timingFile.write(line)
        timingFile.close()
            # Choose random music file
        muxCommand += " -filter_complex '" + complexFilter + "concat=n=" + str(clip_count-1) + ":v=0:a=1[out]' -map '[out]' " + os.path.join(self.imageDir, "muxed.mp3")

        p = subprocess.Popen(muxCommand, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()



        videoGenCommand = 'ffmpeg -y -safe 0 -i ' + os.path.join(self.imageDir, 'timing.ffconcat') + ' ' + os.path.join(self.imageDir, 'out.mp4')
        p = subprocess.Popen(videoGenCommand, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()

        combineCommand = "ffmpeg -y -i " + self.imageDir + "/out.mp4 -i " + os.path.join(self.imageDir, "muxed.mp3") + " -c copy " + self.imageDir + "/combined.mp4"
        p = subprocess.Popen(combineCommand, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()

        if os.path.exists(os.path.join(self.imageDir, "muxed.mp3")):
            os.remove(os.path.join(self.imageDir, "muxed.mp3"))
        os.remove(os.path.join(self.imageDir, "out.mp4") )
        jsonFile = os.path.join(self.imageDir, "imageAnalysis.json")
        with open(jsonFile, 'w') as outfile:
            json.dump(self.clarifaiData, outfile)


    def digestData(self):
        imageCount = 0
        for image in self.clarifaiData['outputs']:
            concepts = image['data']['concepts']
            emotion = self.findEmotion(concepts)
            theme = self.findTheme(concepts)
            product = self.findProduct(self.logoData['outputs'][imageCount], concepts)
            timeOnScreen = {"start":3 * imageCount, "end":3 * imageCount + 3}
            self.imageMeta[imageCount] = {"emotion" : emotion, "theme" : theme, "product" : product, "timing" : timeOnScreen}
            print(json.dumps(concepts,indent=4))
            imageCount += 1
            jsonFile = os.path.join(self.imageDir, "videoMeta.json")
            with open(jsonFile, 'w') as outfile:
                json.dump(self.imageMeta, outfile)
        print(json.dumps(self.imageMeta,indent=4))

    def findEmotion(self, concepts):
        happyList = ['happy', 'happiness']
        adventureList = ['outdoors']
        partyList = ['joy']
        determinedEmotion = 'happy'

        for concept in concepts:
            if concept['name'] in happyList:
                determinedEmotion = "happy"
                break
            if concept['name'] in adventureList:
                determinedEmotion = "adventure"
                break
            if concept['name'] in partyList:
                determinedEmotion = "party"
                break
        return determinedEmotion

    def findTheme(self, concepts):
        return concepts[0]['name']

    def findProduct(self, logoConcepts, concepts):
        product = "Could not find"
        if len(logoConcepts) > 0:
            if 'regions' in logoConcepts['data']:
                if len(logoConcepts['data']['regions']) > 0:
                    product = logoConcepts['data']['regions'][0]['data']['concepts'][0]['name']
        else:
            product = concepts[1]['name']
        return product
