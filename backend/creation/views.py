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

OVERVIEW_URL = "b86291ee608841399604117f4b590b38"
CREATION2020_URL = "9ba1296eeef04ba4974795bdc0f39b43"
TIMELINE_URL = "6793df94445b48abb67ed5cbf87c666e"
PASTCREATION_URL = "4ba3ecc40c0545ad95b3709d4e6f8024"
CONTACTUS_URL = "9b8a36b7d2714e578a7c77c38bc903fe"

# Create your views here.

@api_view(['Get'])
def creation(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", OVERVIEW_URL)), 
    Thread(target=part, args=("creation2020", CREATION2020_URL)), 
    Thread(target=part, args=("timeline", TIMELINE_URL)),
    Thread(target=part, args=("pastcreation", PASTCREATION_URL)), 
    Thread(target=part, args=("contactus", CONTACTUS_URL))]

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


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)