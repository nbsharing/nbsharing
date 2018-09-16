from flask import Flask, request, send_from_directory
from . import main
from os import path

app = Flask(__name__)

@app.route("/api/convert", methods=["GET", "POST"])
def hello_http():
    return main.hello_http(request)

@app.route('/<path:filename>')
def download_file(filename):
    folder = path.join(path.abspath(path.dirname(__file__)), "../docs")
    return send_from_directory(folder, filename)

