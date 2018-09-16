from nbconvert import HTMLExporter
import nbformat
from flask import abort
import hashlib
from google.cloud import storage
from io import StringIO


BUCKET_NAME = "cdn.nbsharing.com"
BUCKET_URL_PREFIX = "https://"

def hash_notebook(notebook_file):
    h = hashlib.sha256()
    h.update(notebook_file.read())
    notebook_file.seek(0)
    return h.hexdigest()[:32]

def convert_notebook_to_html(notebook_file):
    notebook = nbformat.read(notebook_file, as_version=4)
    notebook_file.seek(0)
    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_notebook_node(notebook)
    return StringIO(body)

def upload_to_gcloud(file, destination_blob_name, content_type=None):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, predefined_acl="publicRead", content_type=content_type)


def hello_http(request):
    try:
        notebook_file = request.files["notebook"].stream
        notebook_html = convert_notebook_to_html(notebook_file)
        
        hn = hash_notebook(notebook_file)
        notebook_ipynb_filename = "notebook/" + hn + ".ipynb"
        notebook_html_filename = "html-default/" + hn + ".html"
        
        upload_to_gcloud(notebook_file, notebook_ipynb_filename)
        upload_to_gcloud(notebook_html, notebook_html_filename, content_type="text/html")
    except Exception:
        return "Oops! 🙊 Something went wrong. Please try again."
    
    return BUCKET_URL_PREFIX + BUCKET_NAME + "/" + notebook_html_filename