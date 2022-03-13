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

OVERVIEW_URL = "cb60de72538846a490b990018cc63486"
WORKSHOPREGISTRATION_URL = "8f926020d525419aa708e34021d49e84"
DATASCIENCE_URL = "57ede608b6b042bea480ee93a966c185"
WEBDEV_URL = "0ededa3f0ed440a9a31c7fbdc4c4dbeb"
MICROSOFTEXCELVBA_URL = "00481d1cf57041cb8626ba07215ff5aa"

# Create your views here.

@api_view(['Get'])
def externalworkshops(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", OVERVIEW_URL)), 
    Thread(target=part, args=("workshopregistration", WORKSHOPREGISTRATION_URL)), 
    Thread(target=part, args=("datascience", DATASCIENCE_URL)),
    Thread(target=part, args=("webdev", WEBDEV_URL)), 
    Thread(target=part, args=("microsoftexcelvba", MICROSOFTEXCELVBA_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["workshopregistration"]
    data += components["datascience"]
    data += components["webdev"]
    data += components["microsoftexcelvba"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)