import os
import config
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

class ImageRecog:

    def __init__(self, imageDir):
        self.app = ClarifaiApp(api_key=config.conf['clarify_key'])
        self.model = self.app.models.get("general-v1.3")
        self.imageDir = imageDir
        os.system('ffmpeg -r 1/3 -i ' + self.imageDir + '/image_%04d.png ' + self.imageDir + '/out.mp4')

    def analyzeImages(self):
        imageArray = []
        for the_file in os.listdir(self.imageDir):
            image = ClImage(file_obj=open(os.path.join(self.imageDir, the_file), 'rb'))
            imageArray.append(image)
        response = self.model.predict(imageArray)
        return response
