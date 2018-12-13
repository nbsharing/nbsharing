from nbconvert import HTMLExporter
import nbformat
from flask import make_response
import hashlib
from google.cloud import storage
from io import StringIO
from os import path
import logging


BUCKET_NAME = "cdn.nbsharing.com"
BUCKET_URL_PREFIX = "https://"
HTML_TEMPLATE_PATH = path.join(path.abspath(path.dirname(__file__)), "templates/nbsharing_default.tpl")

def cors(f):
    def new_f(*args, **kwargs):
        r = f(*args, **kwargs)
        flask_response = make_response(r)
        flask_response.headers['Access-Control-Allow-Origin'] = '*'
        return flask_response
    return new_f

def hash_notebook(notebook_file):
    h = hashlib.sha256()
    h.update(notebook_file.read())
    notebook_file.seek(0)
    return h.hexdigest()[:32]

def convert_notebook_to_html(notebook_file):
    notebook = nbformat.read(notebook_file, as_version=4)
    notebook_file.seek(0)
    html_exporter = HTMLExporter()
    html_exporter.template_file = HTML_TEMPLATE_PATH
    body, _ = html_exporter.from_notebook_node(notebook)
    return StringIO(body)

def upload_to_gcloud(file, destination_blob_name, content_type=None):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, predefined_acl="publicRead", content_type=content_type)

@cors
def nbconvert(request):
    try:
        notebook_file = request.files["notebook"].stream
        notebook_html = convert_notebook_to_html(notebook_file)
        
        hn = hash_notebook(notebook_file)
        notebook_ipynb_filename = "notebook/" + hn + ".ipynb"
        notebook_html_filename = "html-default/" + hn + ".html"
        
        upload_to_gcloud(notebook_file, notebook_ipynb_filename)
        upload_to_gcloud(notebook_html, notebook_html_filename, content_type="text/html")
    except Exception as e:
        logging.exception("Couldn't transform the notebook")
        return "Oops! 🙊 Something went wrong. Please try again."
    
    return BUCKET_URL_PREFIX + BUCKET_NAME + "/" + notebook_html_filename
