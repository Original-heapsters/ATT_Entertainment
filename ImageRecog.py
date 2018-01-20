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

    def analyzeImages(self):
        imageArray = []
        for the_file in os.listdir(self.imageDir):
            image = ClImage(file_obj=open(os.path.join(self.imageDir, the_file), 'rb'))
            imageArray.append(image)
        response = self.model.predict(imageArray)
        return response
