import requests
import os
import uuid
import magic
import base64
import json

from time import time
from datetime import datetime

from flask import (Blueprint, jsonify, request)
from werkzeug.exceptions import abort

from .db import Object, db, Image

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
    def insert_tags(self, image, response):
        response_dict = json.loads(response.content.decode('utf-8'))
        response_list = response_dict.get('result').get('tags')
            
        for current in response_list:
            tag = current.get('tag').get('en')
            object = Object(name=tag)
            image.objects.append(object)
            db.session.commit()
                    
    def detect_objs(self, request_body):
        label = request_body.get("label")
        if not label:
            label = name_gen()

        # DEBUG
        image = Image(data="foo".encode(), label=label)
        db.session.add(image)
        db.session.commit()

        if request_body.get('detection_flag') == "True":
            image_data = request_body.get('data')
            response = requests.post(
                IMAGGA_TAGS_ENDPOINT,
                auth=(API_KEY, API_SECRET),
                data={'image': base64.b64decode(image_data.encode())})
            
            self.insert_tags(image, response)

        return str(image.id)

    def detect_objs_by_url(self, request_body):
        label = request_body.get("label")
        if not label:
            label = name_gen()

        # DEBUG
        image = Image(label=label)
        db.session.add(image)
        db.session.commit()
        
        if request_body.get('detection_flag') == "True":
            image_url = request_body.get("image_url")
            response = requests.get(
                f'{IMAGGA_TAGS_ENDPOINT}?image_url={image_url}',
                auth=(API_KEY, API_SECRET))

            self.insert_tags(image, response)

        # DEBUG
        return "Drokk"


@bp.route('/images', methods=['GET', 'POST'])
def retrieve_image_data():
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

        handler = Request_Handler()

        request_body = request.get_json()
        
        # DEBUG
        headers = request.headers.get('Content-type')
                
        if request_body.get('data'):
            response = handler.detect_objs(request_body)
            return response
        elif request_body.get("image_url"):
            response = handler.detect_objs_by_url(request_body)
            return response
        else:
            abort(400, "provide 'image_data' or 'image_url' in the json body of the request")
    elif request.method == 'GET':
        if request.args:
            filters = request.args.to_dict().get('objects').split(",")

            for filter in filters:
                obj_match = Object.query.filter_by(name=filter).all()
                for obj in obj_match:
                    print(Image.query.get(obj.image_id))
            return "Grok"
        else:
            all_images = Image.query.all()
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
    image = Image.query.get(imageId)
    # print(image.id)
    # print(image.label)
    # print(image.objects)

    return jsonify(id=image.id, label=image.label, objects=str(image.objects))
