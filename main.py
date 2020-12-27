import os
from flask import Flask, request, render_template
from flask import Response

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/train", methods=['POST'])
@cross_origin()
def train_data():

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict_data():


port = int(os.getenv("PORT", 5001))
if __name__ == "__main__":
    app.run(port=port, debug=True)
