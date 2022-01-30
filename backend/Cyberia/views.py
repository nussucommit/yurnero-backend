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

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')

# Create your views here.

@api_view(['Get'])
def Cyberia(request):
    data = []
    # data += overview()
    result = dict()
    result["result"] = data
    benefit()
    return Response(result, status=status.HTTP_200_OK)


def overview():
    url = 'https://api.notion.com/v1/blocks/40712ecd5d6246aab46d9d51442c1727/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    return parse(data)


def benefit():
    url = 'https://api.notion.com/v1/blocks/1b95121ff4e24ab38c155c99c42675d9/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    data = response.json()
    print(parse(data))
    # print(data)
    # return parse(data)

def time():
    url = 'https://api.notion.com/v1/blocks/95e9bd5dd0394a2bb8e6b5c10b3433b3/children'
    headers = {'Notion-Version': version, 'Authorization': token}


def registriation():
    url = 'https://api.notion.com/v1/blocks/8bfb13152625483f996f26c2e7d2b371/children'
    headers = {'Notion-Version': version, 'Authorization': token}

def acadia_training():
    url = 'https://api.notion.com/v1/blocks/d36eabdea553461dadf34410534deb25/children'
    headers = {'Notion-Version': version, 'Authorization': token}

def trainers():
    url = 'https://api.notion.com/v1/blocks/949adb5dff604986be8785c4d65d7c70/children'
    headers = {'Notion-Version': version, 'Authorization': token}

def contact():
    url = 'https://api.notion.com/v1/blocks/139602eef0454c4aa124dc5363b272a0/children'
    headers = {'Notion-Version': version, 'Authorization': token}




