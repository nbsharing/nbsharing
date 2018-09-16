from flask import Flask, request, send_from_directory, send_file
from . import main
from os import path

app = Flask(__name__)

@app.route("/nbconvert", methods=["GET", "POST"])
def nbconvert():
    return main.nbconvert(request)

@app.route('/')
def index():
    filepath = path.join(path.abspath(path.dirname(__file__)), "../docs/index.html")
    return send_file(filepath)

@app.route('/<path:filename>')
def download_file(filename):
    folder = path.join(path.abspath(path.dirname(__file__)), "../docs")
    return send_from_directory(folder, filename)

