from cgi import parse_header
from typing import List
from urllib import response
from rest_framework.decorators import api_view
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import os
from backend.notion_api_parser import *
import requests
from threading import Thread

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')
components = dict()

NOTION_PAGE_URL = 'https://api.notion.com/v1/blocks/{blockid}/children'
NOTION_PAGE = 'https://api.notion.com/v1/blocks/{blockid}'
NOTION_HEADER = {'Notion-Version': version, 'Authorization': token}

YIH_CONTACTS = "a4be329fe1ed49f08b0c0c65a1293c2f"
AS8_CONTACTS = "9085515cae9a427e98a2d18f946527e6"
CONTACT_US = "954f3393bbd24c42958ead8d3ce806be"
SUBSCRIBE_LIST = "5b865a50b2ed473dbb32da1a0d170bfc"

@api_view(["Get"])
def contacts(data):
    data = dict()

    thread = [Thread(target=part, args=("contactus", CONTACT_US))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    data["contactus"] = dict()

    contact_types = ["general_enquiries", "marketing_and_sponsorship", "workshop_enquiries" ]
    for contact_type in contact_types:
        data["contactus"][contact_type] = []

    index = 0

    for paragraph in components["contactus"]:
        print(type(paragraph))
        # Notion separate the group of paragraph with an empty paragrapg
        if (len(paragraph["content"]) == 0):
            index += 1
            continue;
        data["contactus"][contact_types[index]].append(paragraph)

    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def address(data):
    data = dict()

    thread = [Thread(target=part, args=("yih", YIH_CONTACTS)),
              Thread(target=part, args=("as8", AS8_CONTACTS))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    locations = ["yih", "as8"]
    data["locations"] = dict()

    for location in locations:
        unfilteredComponent = components[location]
        filteredComponent = list(filter(lambda x: len(x["content"]) != 0, unfilteredComponent))
        data["locations"][location] = dict()
        data["locations"][location]["address"] = filteredComponent[:2]
        data["locations"][location]["opening_hour"] = filteredComponent[2:]

    data["contactus"] = dict()

    return Response(data, status=status.HTTP_200_OK)


@api_view(['Get'])
def subscribe(data):
    data = dict()

    thread = [Thread(target=part, args=("subscribe_list", SUBSCRIBE_LIST))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    data["subscribe_list"] = components["subscribe_list"]
    return Response(data, status=status.HTTP_200_OK)
def part(component, id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)


