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


def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)






