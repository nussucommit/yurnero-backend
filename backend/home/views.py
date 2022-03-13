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

NOTION_PAGE_URL = 'https://api.notion.com/v1/blocks/{blockid}/children'
NOTION_HEADER = {'Notion-Version': version, 'Authorization': token}

@api_view(['Get'])
def home(request):
  components = dict()
  
  component_list = [("training_workshops", "c5cdbf3484cc4f77821e0691b8b4a47b"),
                    ("elevate_creativity", "aab5e676774444188471c7b7a105c52c"),
                    ("study_print_scan", "efea5f3b0a8d4af4879798c6a347f3bc")]
  threads = [Thread(target=part, args=(components, comp_name, comp_id)) for (comp_name, comp_id) in component_list]

  for t in threads:
        t.start()

  for t in threads:
        t.join()

  return Response(components, status=status.HTTP_200_OK)


def part(components, component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)