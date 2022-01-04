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
    print(response.status_code)
    print(response.json())


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

    response = dc.retrieve_all_image_data()
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_id(6)
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_tags(params={'objects': "dog,cat"})
    print(response.status_code)
    print(response.json())

    # response = dc.retrieve_image_data_by_tags(params={'objects': "sun,wind"})
    # print(response.status_code)
    # print(response.json())

    # with label and image detection
    # payload = {"label":"robot.jpg",
    #            "image_path":"/home/legionarius/images/robot1.jpg",
    #            "image_url":"",
    #            "detection_flag": "True"}
    # response = dc.upload_image(request_body=payload, file_path="/home/legionarius/images/robot1.jpg")
    # print(response.status_code)
    # print(response.json())
    
    # with label no image detection
    # payload = {"label":"robot.jpg",
    #            "image_path":"/home/legionarius/images/robot1.jpg",
    #            "image_url":"",
    #            "detection_flag": "False"}
    # response = dc.upload_image(request_body=payload, file_path="/home/legionarius/images/robot1.jpg")
    # print(response.status_code)
    # print(response.json())

    # without label no image detection
    # payload = { "image_path":"/home/legionarius/images/robot1.jpg",
    #            "image_url":"",
    #            "detection_flag": "False"}
    # response = dc.upload_image(request_body=payload, file_path="/home/legionarius/images/robot1.jpg")
    # print(response.status_code)
    # print(response.json())

    # payload = {"image_path": "",
    #            "image_url": "https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg",
    #            "detection_flag": "True"}
    # response = dc.upload_image(request_body=payload)
    # print(response.status_code)
    # print(response.json())

    # payload = {"image_path": "",
    #            "image_url": "https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"}
    # response = dc.upload_image(request_body=payload)
    # print(response.status_code)
    # print(response.json())
    
    # url = (f'https://en.wikipedia.org/wiki/American_Staffordshire_Terrier#'
    #        f'/media/File:AMERICAN_STAFFORDSHIRE_TERRIER,_Zican%E2%80%99s_Bz_E'
    #        f'z_Dragon_(24208348891).2.jpg')
    
    # payload = {"image_path": "",
    #            "image_url": url,
    #            "detection_flag": "True"}
    # response = dc.upload_image(request_body=payload)
    # print(response.status_code)
    # print(response.json())
    
    # url = (f'https://www.publicdomainpictures.net/pictures/110000/velka/sumatran-tiger-1414587733tzH.jpg')
    
    # payload = {"image_path": "",
    #            "image_url": url,
    #            "detection_flag": "True"}
    # response = dc.upload_image(request_body=payload)
    # print(response.status_code)
    # print(response.json())