import config
from clarifai import rest
from clarifai.rest import ClarifaiApp

class ImageRecog:

    def __init__(self):
        self.app = ClarifaiApp(api_key=config['clarify_key'])
        self.model = self.app.models.get("food-items-v1.0")

    def analyzeImage(self):
        final = self.model.predict_by_url(url='https://thumbs.dreamstime.com/z/man-eating-banana-happy-over-white-background-52475806.jpg')
        return final
