import sys
from os import environ

import requests
from detector.images_client import ImagesClient


def check_server(client):
    try:
        client.retrieve_image_data_by_id(id="")
    except requests.exceptions.ConnectionError:
        print("Flask Server Is Not Running")
        sys.exit(1)


class TestImages:
    @classmethod
    def setup_class(cls):
        cls.dc = ImagesClient()
        check_server(cls.dc)

    def test_retrieve_all_image_data(self):
        response = self.dc.retrieve_all_image_data()
        assert(response.status_code == 200)
        assert(response.ok)

    def test_retrieve_image_data_by_id(self):
        response = self.dc.retrieve_image_data_by_id(id=1)
        assert(response.status_code == 200)
        assert(response.ok)

    def test_retrieve_image_data_by_tags(self):
        params = {'objects': "dog,cat"}
        response = self.dc.retrieve_image_data_by_tags(params=params)
        assert(response.status_code == 200)
        assert(response.ok)

    def test_upload_image_by_path(self):
        payload = {"detection_flag": "False"}
        path = "/".join([environ['HOME'], "images/robot1.jpg"])
        response = self.dc.upload_image(request_body=payload,
                                        file_path=path)
        assert(response.status_code == 200)
        assert(response.ok)

    def test_upload_image_by_url(self):
        url = (f'https://imagga.com/static/images/tagging/wind-farm-538576_'
               f'640.jpg')
        payload = {"label": "robot.jpg",
                   "image_path": "",
                   "image_url": url,
                   "detection_flag": "True"}
        response = self.dc.upload_image(request_body=payload)
        assert(response.status_code == 200)
        assert(response.ok)
