import json
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    indexObj = {"one":"two"}
    return json.dumps(indexObj)

@app.route('/complexjson')
def complexJson():
    sample = {'ObjectInterpolator': 1629,  'PointInterpolator': 1675, 'RectangleInterpolator': 2042}

    return json.dumps(sample)
@app.route('/yodawg')
def yodawg():
    return "Yo dawg, I heard you like testing endpoints so i put and endpoint in your endpoint"

if __name__ == "__main__":
  app.run(port=8080, debug=True)
