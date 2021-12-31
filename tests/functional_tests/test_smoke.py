import requests
import sys

from detector.detector_client import DetectorClient


def check_server(client):
    try:
        client.retrieve_image_data_by_id(id="")
    except requests.exceptions.ConnectionError:
        print("Flask Server Is Not Running")
        sys.exit(1)
        

class TestImages:
    @classmethod
    def setup_class(cls):
        cls.dc = DetectorClient()
        check_server(cls.dc)
        
    def test_retrieve_all_image_data(self):
        response = self.dc.retrieve_all_image_data()
        assert(response.ok)
            
    def test_retrieve_image_data_by_id(self):
        response = self.dc.retrieve_image_data_by_id(id="robot1.jpg")
        assert(response.ok)
        
    def test_retrieve_image_data_by_tags(self):
        response = self.dc.retrieve_image_data_by_tags(params={'objects': "dog,cat"})
        assert(response.ok)
        
    def test_upload_image_by_path(self):
        payload = {"label":"robot.jpg",
                "image_path":"/home/legionarius/images/robot1.jpg", 
                "image_url":"",
                "detection_flag": "False"}
        response = self.dc.upload_image(request_body=payload)
        assert(response.ok)
        
    def test_upload_image_by_url(self):
        payload = {"label":"robot.jpg",
                "image_path":"", 
                "image_url":"https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg",
                "detection_flag": "True"}
        response = self.dc.upload_image(request_body=payload)
        assert(response.ok)
