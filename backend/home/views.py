from rest_framework.decorators import api_view
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path

import os
import requests
from backend.notion_api_parser import parse

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')

NOTION_PAGE_URL = 'https://api.notion.com/v1/blocks/{blockid}/children'
NOTION_HEADER = {'Notion-Version': version, 'Authorization': token}


# Create your views here.
@api_view(['Get'])
def training_workshops(request):
    TRAINING_WORKSHOPS_URL = 'c5cdbf3484cc4f77821e0691b8b4a47b'
    data = [get_parsed_data(TRAINING_WORKSHOPS_URL)]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['Get'])
def elevate_creativity(request):
    ELEVATE_CREATIVITY_URL = 'aab5e676774444188471c7b7a105c52c'
    data = [get_parsed_data(ELEVATE_CREATIVITY_URL)]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['Get'])
def study_print_scan(request):
    STUDY_PRINT_SCAN_URL = 'efea5f3b0a8d4af4879798c6a347f3bc'
    data = [get_parsed_data(STUDY_PRINT_SCAN_URL)]
    return Response(data, status=status.HTTP_200_OK)


def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    return parse(data)
