from flask import Flask
from flask import render_template
from flask import Response
from flask import url_for
from main import FacialRecognition
import os

app = Flask(__name__)

facrec = FacialRecognition()
facrec.train_model()

@app.route("/")
def home():
    return render_template('index.html', user = "Arav")

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    facrec.generate_hls_stream()  # Generate the HLS stream
    return render_template('video.html')

@app.route('/hls/<filename>')
def hls_file(filename):
    return Response(
        open(os.path.join("static/hls", filename), 'rb'),
        mimetype='application/vnd.apple.mpegurl' if filename.endswith('.m3u8') else 'video/MP2T'
    )

if __name__ == '__main__':
    app.run(debug = True)