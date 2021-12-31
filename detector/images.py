import requests
import os
import uuid
import magic
import base64

from time import time
from datetime import datetime

from flask import (Blueprint, jsonify, request)
from werkzeug.exceptions import abort

from .db import db, Image

IMAGGA_TAGS_ENDPOINT = "https://api.imagga.com/v2/tags"
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]

bp = Blueprint('image', __name__)

def get_mime_type(file_path):
    try:
        mime_type = magic.from_file(file_path).split(" ")[0]
    except (FileNotFoundError, IndexError):
        return None
    return mime_type

def name_gen(name_base="image"):
    """[summary]
    creates a friendly name for the image
    Args:
        base_name (str, optional): [description]. Defaults to "image".

    Returns:
        [str]: <name_base>_<month>_<year>_<epoch seconds>_<epoch millisenconds>
    """
    epoch_time = time()
    month_year = datetime.fromtimestamp(epoch_time).strftime('%m_%Y')
    return f'{name_base.replace(".", "_")}_{month_year}_{str(epoch_time).replace(".", "_")}'


def id_gen(id_base="image"):
    """[summary]
    creates a label for the db
    Args:
        base_name (str, optional): [description]. Defaults to "image".

    Returns:
        [str]: <id_base>-<uuid>
    """
    return "-".join([id_base.replace(".", "-"), str(uuid.uuid4())])


class Request_Handler():
    def detect_objs_by_path(self, image_data):
        """[summary]

        Args:
            image_data ([str): path/to/image_file

        Returns:
            [type]: [description]
        """
        # with open(image_path, 'rb') as file_obj:
        #     response = requests.post(
        #         IMAGGA_TAGS_ENDPOINT,
        #         auth=(API_KEY, API_SECRET),
        #         files={'image': file_obj})
        # return response.content
        
        response = requests.post(
            IMAGGA_TAGS_ENDPOINT,
            auth=(API_KEY, API_SECRET),
            data={'image': base64.b64decode(image_data.encode())})
        
        # DEBUG
        return str(response.json())

    def detect_objs_by_url(self, image_url):
        """[summary]

        Args:
            image_url ([str]): image_url

        Returns:
            [type]: [description]
        """
        response = requests.get(
            f'{IMAGGA_TAGS_ENDPOINT}?image_url={image_url}',
            auth=(API_KEY, API_SECRET))
        return response.content

        # DEBUG
        return str(response.json())


@bp.route('/images', methods=['GET', 'POST'])
def retrieve_image_data():
    """[summary]

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        """[summary]
        Send a JSON request body including an image file or URL, an optional label for the
        image, and an optional field to enable object detection.
        
        Returns a HTTP 200 OK with a JSON response body including the image data, its label
        (generate one if the user did not provide it), its identifier provided by the persistent data
        store, and any objects detected (if object detection was enabled).
        Returns:
            [type]: [description]
        """
        db.session.add(Image(data="foo".encode(), label="test"))
        db.session.commit()
        handler = Request_Handler()

        request_body = request.get_json()
        
        # DEBUG
        headers = request.headers.get('Content-type')

        image_url = request_body.get("image_url")
        label = request_body.get("label")
        image_data = request_body.get('data')
                
        if image_data:
            response = handler.detect_objs_by_path(image_data)
            return response
        elif image_url:
            response = handler.detect_objs_by_url(image_url)
            return response
        else:
            abort(400, "provide 'image_data' or 'image_url' in the json body of the request")
    elif request.method == 'GET':
        if request.args:
            """[summary]
            Returns a HTTP 200 OK with a JSON response body containing only images that have
            the detected objects specified in the query parameter.
            Returns:
                [type]: [description]
            """
            return str(request.args.get('objects'))
        else:
            """[summary]
            Returns HTTP 200 OK with a JSON response containing all image metadata.
            Returns:
                [type]: [description]
            """
            
            return str(Image.query.all())
        
@bp.route('/images/<imageId>', methods=['GET'])
def retrieve_data_by_id(imageId):
    """[summary]
    Returns HTTP 200 OK with a JSON response containing image metadata for the
    specified image.
    Args:
        imageId ([type]): [description]

    Returns:
        [type]: [description]
    """
    return imageId
