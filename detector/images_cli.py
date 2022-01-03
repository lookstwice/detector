#!/usr/bin/env python
import requests
from images_client import ImagesClient
import sys
import argparse


def check_server(client):
    try:
        client.retrieve_image_data_by_id(id="")
    except requests.exceptions.ConnectionError:
        print("Flask Server Is Not Running")
        sys.exit(1)


def main(args):
    print(args)


def act1(args):
    print('act1')
    print(args)


def act2(args):
    print('act2')
    print(args)


def get_all():
    response = dc.retrieve_all_image_data()
    print(response)
    print(response.content)


if __name__ == '__main__':
    dc = ImagesClient()
    check_server(dc)

    # parser = argparse.ArgumentParser()

    # parser.add_argument("--get-all")
    # parser.add_argument("--get-by-id")
    # parser.add_argument("--get-by-objs")
    # parser.add_argument("--upload")

    # args = parser.parse_args()
    # print(args.get_all)

    # main(args)

    # response = dc.retrieve_all_image_data()
    # print(response)
    # print(response.content)

    # response = dc.retrieve_image_data_by_id(2)
    # print(response)
    # print(response.content)

    # response = dc.retrieve_image_data_by_tags(params={'objects': "dog,cat"})
    # print(response)
    # print(response.content)

    # response = dc.retrieve_image_data_by_tags(params={'objects': "sun,wind"})
    # print(response)
    # print(response.content)

    # with label and image detection
    # payload = {"label":"robot.jpg",
    #            "image_path":"/home/legionarius/images/robot1.jpg",
    #            "image_url":"",
    #            "detection_flag": "True"}
    # response = dc.upload_image(request_body=payload, file_path="/home/legionarius/images/robot1.jpg")
    # print(response)
    # print(response.content)
    
    # with label no image detection
    # payload = {"label":"robot.jpg",
    #            "image_path":"/home/legionarius/images/robot1.jpg",
    #            "image_url":"",
    #            "detection_flag": "False"}
    # response = dc.upload_image(request_body=payload, file_path="/home/legionarius/images/robot1.jpg")
    # print(response)
    # print(response.content)

    # without label no image detection
    # payload = { "image_path":"/home/legionarius/images/robot1.jpg",
    #            "image_url":"",
    #            "detection_flag": "False"}
    # response = dc.upload_image(request_body=payload, file_path="/home/legionarius/images/robot1.jpg")
    # print(response)
    # print(response.content)

    # payload = {"image_path": "",
    #            "image_url": "https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg",
    #            "detection_flag": "True"}
    # response = dc.upload_image(request_body=payload)
    # print(response)
    # print(response.content)

    payload = {"image_path": "",
               "image_url": "https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"}
    response = dc.upload_image(request_body=payload)
    print(response)
    print(response.content)