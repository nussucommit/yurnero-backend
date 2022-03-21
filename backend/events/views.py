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

CREATION_OVERVIEW_URL = "b86291ee608841399604117f4b590b38"
CREATION_CREATION2020_URL = "9ba1296eeef04ba4974795bdc0f39b43"
CREATION_TIMELINE_URL = "6793df94445b48abb67ed5cbf87c666e"
CREATION_PASTCREATION_URL = "4ba3ecc40c0545ad95b3709d4e6f8024"
CREATION_CONTACTUS_URL = "9b8a36b7d2714e578a7c77c38bc903fe"

CHARITEACH_OVERVIEW_URL = "1a5fc7e7956b458a8edcb0bd8451921e"
CHARITEACH_WHATISCHARITEACH_URL = "160d7ed49b234e5f8d88dd778d3346d8"
CHARITEACH_ABOUTCHARITEACH_URL = "43dba577cdb4406882c6a17b27a0a90a"
CHARITEACH_CONTACTUS_URL = "929fad0ccd9743d19c3b50faf2d70549"

# Create your views here.


@api_view(['Get'])
def cyberia(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", "40712ecd5d6246aab46d9d51442c1727")), 
    Thread(target=part, args=("benefits", "1b95121ff4e24ab38c155c99c42675d9")), 
    Thread(target=part, args=("time", "95e9bd5dd0394a2bb8e6b5c10b3433b3")),
    Thread(target=part, args=("registriation", "8bfb13152625483f996f26c2e7d2b371")), 
    Thread(target=part, args=("acadia_training", "d36eabdea553461dadf34410534deb25")),
    Thread(target=part, args=("trainers", "949adb5dff604986be8785c4d65d7c70")),
    Thread(target=part, args=("contact", "139602eef0454c4aa124dc5363b272a0"))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["benefits"]
    data += components["time"]
    data += components["registriation"]
    data += components["acadia_training"]
    data += components["trainers"]
    data += components["contact"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


@api_view(['Get'])
def creation(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", CREATION_OVERVIEW_URL)), 
    Thread(target=part, args=("creation2020", CREATION_CREATION2020_URL)), 
    Thread(target=part, args=("timeline", CREATION_TIMELINE_URL)),
    Thread(target=part, args=("pastcreation", CREATION_PASTCREATION_URL)), 
    Thread(target=part, args=("contactus", CREATION_CONTACTUS_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["creation2020"]
    data += components["timeline"]
    data += components["pastcreation"]
    data += components["contactus"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


@api_view(['Get'])
def chariteach(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", CHARITEACH_OVERVIEW_URL)), 
    Thread(target=part, args=("whatischariteach", CHARITEACH_WHATISCHARITEACH_URL)), 
    Thread(target=part, args=("aboutchariteach", CHARITEACH_ABOUTCHARITEACH_URL)),
    Thread(target=part, args=("contactus", CHARITEACH_CONTACTUS_URL))]

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