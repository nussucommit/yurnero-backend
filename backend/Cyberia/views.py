from urllib import response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import os
import requests
from Cyberia.NotionAPIparser import * 
from threading import Thread

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')
components = dict()

# Create your views here.

@api_view(['Get'])
def Cyberia(request):
    data = []
    
    thread = [Thread(target=overview), Thread(target=benefit), 
    Thread(target=time),Thread(target=registriation), Thread(target=trainers),
    Thread(target=acadia_training), Thread(target=contact)]

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


def overview():
    url = 'https://api.notion.com/v1/blocks/40712ecd5d6246aab46d9d51442c1727/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    components["overview"] = parse(data)


def benefit():
    url = 'https://api.notion.com/v1/blocks/1b95121ff4e24ab38c155c99c42675d9/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    components["benefits"] = parse(data)


def time():
    url = 'https://api.notion.com/v1/blocks/95e9bd5dd0394a2bb8e6b5c10b3433b3/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    components["time"] = parse(data)


def registriation():
    url = 'https://api.notion.com/v1/blocks/8bfb13152625483f996f26c2e7d2b371/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    components["registriation"] = parse(data)

def acadia_training():
    url = 'https://api.notion.com/v1/blocks/d36eabdea553461dadf34410534deb25/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    components["acadia_training"] = parse(data)

def trainers():
    url = 'https://api.notion.com/v1/blocks/949adb5dff604986be8785c4d65d7c70/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    components["trainers"] = parse(data)

def contact():
    url = 'https://api.notion.com/v1/blocks/139602eef0454c4aa124dc5363b272a0/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    components["contact"] = parse(data)




