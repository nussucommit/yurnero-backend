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

OVERVIEW_URL = "a48c58b53a3d4286b8dd2c9dfbbc6281"
OPERATINGHOURSE_URL = "6d4a6bbd728743ee8f67ee7a20f5674d"
PRINTINGRATES_URL = "20ff6a061eff4b80b1f08cf9ddc2dbe4"

# Create your views here.

@api_view(['Get'])
def computercentres(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", OVERVIEW_URL)), 
    Thread(target=part, args=("operatinghours", OPERATINGHOURSE_URL)), 
    Thread(target=part, args=("printingrates", PRINTINGRATES_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["operatinghours"]
    data += components["printingrates"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)