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

OURFAMILY_URL = "513571555db74a979c9c4739f1dbaf1d"
VISION_URL = "8bed1bd454ee476eb8bf7bdfba2e0005"
MISSION_URL = "6e3f4b1683e64dffae8d647eff063604"
STRUCTURE_OVERVIEW_URL = "bae5bd180cd44b8587276611caf1df98"
STRUCTURE_MARKETERS_URL = "35ab9f1c24dd4cc98ad3b58972da50d8"
STRUCTURE_PUBLICITY_URL = "eb2f90d1cc16411c9b7677fd6c7d57b3"
STRUCTURE_TECHNICAL_URL = "89ad59be01ab4665a547bf50caaa33b8"
STRUCTURE_TRAINING_URL = "63ef470f57ef4594b61bceb26a118f4c"
STRUCTURE_WELFARE_URL = "e06716cb9539415da457761ab2649031"
STRUCTURE_OPL_URL = "dc70316dbf754958ac22cd3859c36e9e"
MANAGEMENT_COMMITTEE_URL = "10c007ccea174df9a5f1f2b97304ea5d"
OVERVIEW_URL = "6aeaf3319bad46d9bbcde5108b97b747"

@api_view(['Get'])
def vision_mission(request):
    data = []
    
    thread = [Thread(target=part, args=("vision", VISION_URL)), 
    Thread(target=part, args=("mission", MISSION_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["vision"]
    data += components["mission"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def structure(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", STRUCTURE_OVERVIEW_URL)), 
    Thread(target=part, args=("marketing", STRUCTURE_MARKETERS_URL)), 
    Thread(target=part, args=("publicity", STRUCTURE_PUBLICITY_URL)),
    Thread(target=part, args=("technical", STRUCTURE_TECHNICAL_URL)),
    Thread(target=part, args=("training", STRUCTURE_TRAINING_URL)),
    Thread(target=part, args=("welfare", STRUCTURE_WELFARE_URL)),
    Thread(target=part, args=("opl", STRUCTURE_OPL_URL)),]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["marketing"]
    data += components["publicity"]
    data += components["technical"]
    data += components["training"]
    data += components["welfare"]
    data += components["opl"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def family(request):
    data = [get_parsed_data(OURFAMILY_URL)]
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def manag_comm(request):
    data = [get_parsed_data(MANAGEMENT_COMMITTEE_URL)]
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def overview(request):
    data = [get_parsed_data(OVERVIEW_URL)]
    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    return parse(data)

def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)
