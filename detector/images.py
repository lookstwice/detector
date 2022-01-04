import base64
import json
import os
import uuid
from datetime import datetime
from time import time

import magic
import requests
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from .db import Image, Object, db

IMAGGA_TAGS_ENDPOINT = "https://api.imagga.com/v2/tags"
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]

DATA_TEST_STUB = "IMAGE_DATA"

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
        tag_list = []

        response_dict = json.loads(response.content.decode('utf-8'))

        result = response_dict.get('result')
        if result:
            tag_list = result.get('tags')

        for current in tag_list:
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
        image_data = request_body.get('data')

        image = self.insert_image(db, label=label, data=image_data)

        if request_body.get('detection_flag') == "True":

            response = requests.post(
                IMAGGA_TAGS_ENDPOINT,
                auth=(API_KEY, API_SECRET),
                data={'image': base64.b64decode(image_data.encode())})

            self.insert_tags(image, response)

        return jsonify(image=image.to_dict())

    def detect_objs_by_url(self, request_body):
        label = request_body.get("label")

        image = self.insert_image(db, label=label)

        if request_body.get('detection_flag') == "True":
            image_url = request_body.get("image_url")
            response = requests.get(
                f'{IMAGGA_TAGS_ENDPOINT}?image_url={image_url}',
                auth=(API_KEY, API_SECRET))

            self.insert_tags(image, response)

        return jsonify(image=image.to_dict())

    def get_images(self, args=None, id=None):
        if args:
            filters = args.to_dict().get('objects').split(",")

            obj_match = Object.query.filter(Object.name.in_(filters))

            results = [f'{Image.query.get(obj.image_id)} tag={obj.name}' 
                       for obj in obj_match]

            return jsonify(results=results)
        elif id:
            image = Image.query.get(id)

            return jsonify(image=image.to_dict())
        else:
            all_images = Image.query.all()

            results = [img.to_dict() for img in all_images]

            return jsonify(images=results)


@bp.route('/images', methods=['GET', 'POST'])
def process_image_data():
    handler = Request_Handler()

    if request.method == 'POST':
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
            response = handler.get_images(request.args)
            return response
        else:
            response = handler.get_images()
            return response


@bp.route('/images/<imageId>', methods=['GET'])
def process_image_data_by_id(imageId):
    handler = Request_Handler()
    response = handler.get_images(id=imageId)
    return response
