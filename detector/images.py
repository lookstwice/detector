import requests
import os
import uuid

from requests.api import get
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

DATA_TEST_STUB = "TEST_DATA"

bp = Blueprint('image', __name__)

def get_mime_type(file_path):
    try:
        mime_type = magic.from_file(file_path).split(" ")[0]
    except (FileNotFoundError, IndexError):
        return None
    return mime_type

def name_gen(name_base="image"):
    epoch_time = time()
    month_year = datetime.fromtimestamp(epoch_time).strftime('%m_%Y')
    return (f'{name_base.replace(".", "_")}_{month_year}_'
            f'{str(epoch_time).replace(".", "_")}')


def id_gen(id_base="image"):
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

    def insert_image(self, db, label=None, data=None):
        data_payload = None
        if not label:
            label = name_gen()
        
        if data:
            data_payload = data.encode()
            
        image = Image(data=data_payload, label=label)
        db.session.add(image)
        db.session.commit()
        
        return image
        
    def detect_objs(self, request_body):
        label = request_body.get("label")

        image = self.insert_image(db, label=label, data=DATA_TEST_STUB)
        
        if request_body.get('detection_flag') == "True":
            image_data = request_body.get('data')
            response = requests.post(
                IMAGGA_TAGS_ENDPOINT,
                auth=(API_KEY, API_SECRET),
                data={'image': base64.b64decode(image_data.encode())})
            
            self.insert_tags(image, response)

        return jsonify(id=image.id, label=image.label, 
                       objects=str(image.objects))

    def detect_objs_by_url(self, request_body):
        label = request_body.get("label")
        
        image = self.insert_image(db, label=label)
        
        if request_body.get('detection_flag') == "True":
            image_url = request_body.get("image_url")
            response = requests.get(
                f'{IMAGGA_TAGS_ENDPOINT}?image_url={image_url}',
                auth=(API_KEY, API_SECRET))

            self.insert_tags(image, response)

        # DEBUG
        return jsonify(id=image.id, label=image.label, 
                       objects=str(image.objects))


@bp.route('/images', methods=['GET', 'POST'])
def retrieve_image_data():
    if request.method == 'POST':
        handler = Request_Handler()

        request_body = request.get_json()
                
        if request_body.get('data'):
            response = handler.detect_objs(request_body)
            return response
        elif request_body.get("image_url"):
            response = handler.detect_objs_by_url(request_body)
            return response
        else:
            abort(400, (f"provide 'image_data' or 'image_url' in the json "
                        "body of the request"))
    elif request.method == 'GET':
        if request.args:
            filters = request.args.to_dict().get('objects').split(",")

            obj_match = Object.query.filter(Object.name.in_(filters))

            results = [f'{Image.query.get(obj.image_id)} tag={obj.name}' 
                       for obj in obj_match]

            return jsonify(results=results)
        else:
            all_images = Image.query.all()

            results = [{"image": str(img), "objects": str(img.objects)} 
                       for img in all_images]

            return jsonify(result=results)

        
@bp.route('/images/<imageId>', methods=['GET'])
def retrieve_data_by_id(imageId):
    image = Image.query.get(imageId)

    return jsonify(id=image.id, label=image.label, objects=str(image.objects))
