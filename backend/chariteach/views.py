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

OVERVIEW_URL = "1a5fc7e7956b458a8edcb0bd8451921e"
WHATISCHARITEACH_URL = "160d7ed49b234e5f8d88dd778d3346d8"
ABOUTCHARITEACH_URL = "43dba577cdb4406882c6a17b27a0a90a"
CONTACTUS_URL = "929fad0ccd9743d19c3b50faf2d70549"

# Create your views here.

@api_view(['Get'])
def chariteach(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", OVERVIEW_URL)), 
    Thread(target=part, args=("whatischariteach", WHATISCHARITEACH_URL)), 
    Thread(target=part, args=("aboutchariteach", ABOUTCHARITEACH_URL)),
    Thread(target=part, args=("contactus", CONTACTUS_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["whatischariteach"]
    data += components["aboutchariteach"]
    data += components["contactus"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)