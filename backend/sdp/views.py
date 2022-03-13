from django.shortcuts import render
from rest_framework.decorators import api_view
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import os
import requests
from backend.notion_api_parser import * 
from threading import Thread

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')
components = dict()

NOTION_PAGE_URL = 'https://api.notion.com/v1/blocks/{blockid}/children'
NOTION_HEADER = {'Notion-Version': version, 'Authorization': token}

OVERVIEW_URL = "11075f8948e04d89b61bc16b97b978f7"
CURRENTAPPLICATIONS_URL = "29b2d08c4eea4a3a95aa0a913a7ec2e0"
CONTACTUS_URL = "a398833a26f0411aa7f702edd4758203"

# Create your views here.

@api_view(['Get'])
def sdp(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", OVERVIEW_URL)), 
    Thread(target=part, args=("currentapplications", CURRENTAPPLICATIONS_URL)), 
    Thread(target=part, args=("contactus", CONTACTUS_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["currentapplications"]
    data += components["contactus"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)