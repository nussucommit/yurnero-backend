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

OVERVIEW_URL = "f02e4f8af490472d952b112e0b22704a"
WORKSHOPREGISTRATION_URL = "f6afd72b4f2149eebbe3622bd5680f4a"
ADOBEPHOTOSHOP_URL = "930ead6d4d124ffa90d3a7e3d4458fd3"
PYTHON_URL = "48c1869d858242bc8287c990afef5518"
MICROSOFTEXCEL_URL = "700cb040f7d14482815b0203296c32e0"
CONTACTUS_URL = "02b1b881b6f24fc3bf48a5f3eb28d345"

# Create your views here.

@api_view(['Get'])
def trainingworkshops(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", OVERVIEW_URL)), 
    Thread(target=part, args=("workshopregistration", WORKSHOPREGISTRATION_URL)), 
    Thread(target=part, args=("adobephotoshop", ADOBEPHOTOSHOP_URL)),
    Thread(target=part, args=("python", PYTHON_URL)), 
    Thread(target=part, args=("microsoftexcel", MICROSOFTEXCEL_URL)), 
    Thread(target=part, args=("contactus", CONTACTUS_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["workshopregistration"]
    data += components["adobephotoshop"]
    data += components["python"]
    data += components["microsoftexcel"]
    data += components["contactus"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)