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
from backend.notion_api_parser import *
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


@api_view(['Get'])
def contacts(data):
    data = []

    thread = [Thread(target=part, args=("yih", YIH_CONTACTS)),
              Thread(target=part, args=("as8", AS8_CONTACTS)),
              Thread(target=part, args=("contactus", CONTACT_US)),
              Thread(target=part, args=("subscribelist", SUBSCRIBE_LIST))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["yih"]
    data += components["as8"]
    data += components["contactus"]
    data += components["subscribelist"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)


