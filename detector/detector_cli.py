#!/usr/bin/env python
import requests
from detector_client import DetectorClient
import sys
import argparse


def check_server(client):
    try:
        client.retrieve_image_data_by_id(id="")
    except requests.exceptions.ConnectionError:
        print("Flask Server Is Not Running")
        sys.exit(1)

if __name__ == '__main__':
    dc = DetectorClient()
    check_server(dc)
    
    response = dc.retrieve_all_image_data()
    print(response)
    print(response.content)
    
    # response = dc.retrieve_image_data_by_id(id="robot1.jpg")
    # print(response)
    # print(response.content)
    
    # response = dc.retrieve_image_data_by_tags(params={'objects': "dog,cat"})
    # print(response)
    # print(response.content)
    
    # payload = {"label":"robot.jpg",
    #            "image_path":"/home/legionarius/images/robot1.jpg", 
    #            "image_url":"",
    #            "detection_flag": "False"}
    # response = dc.upload_image(request_body=payload, file_path="/home/legionarius/images/robot1.jpg")
    # print(response)
    # print(response.content)
        
    # payload = {"label":"robot.jpg",
    #            "image_path":"", 
    #            "image_url":"https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg",
    #            "detection_flag": "True"}
    # response = dc.upload_image(request_body=payload)
    # print(response)
    # print(response.content)
