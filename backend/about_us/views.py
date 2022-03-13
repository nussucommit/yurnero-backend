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

@api_view(['GET'])
def our_family(request):
  components = dict()
  part(components, "our_family", "513571555db74a979c9c4739f1dbaf1d")

  return Response(components, status=status.HTTP_200_OK)

@api_view(['GET'])
def vision_mission(request):
  components = dict()
  
  component_list = [("our_vision", "25c8592d78364ffe9858615312b697c3"),
                    ("our_mission", "6e3f4b1683e64dffae8d647eff063604")]
  threads = [Thread(target=part, args=(components, comp_name, comp_id)) for (comp_name, comp_id) in component_list]

  for t in threads:
        t.start()

  for t in threads:
        t.join()

  return Response(components, status=status.HTTP_200_OK)

@api_view(['GET'])
def our_structure(request):
  components = dict()
  
  component_list = [("overview", "bae5bd180cd44b8587276611caf1df98"),
                    ("marketing", "35ab9f1c24dd4cc98ad3b58972da50d8"),
                    ("publicity", "30f84d227eb54904b392e98e72a949f1"),
                    ("technical", "89ad59be01ab4665a547bf50caaa33b8"),
                    ("training", "63ef470f57ef4594b61bceb26a118f4c"),
                    ("welfare", "e06716cb9539415da457761ab2649031"),
                    ("ops_logs", "dc70316dbf754958ac22cd3859c36e9e")]
  threads = [Thread(target=part, args=(components, comp_name, comp_id)) for (comp_name, comp_id) in component_list]

  for t in threads:
        t.start()

  for t in threads:
        t.join()

  return Response(components, status=status.HTTP_200_OK)

@api_view(['GET'])
def overview(request):
  components = dict()
  part(components, "overview", "6aeaf3319bad46d9bbcde5108b97b747")

  return Response(components, status=status.HTTP_200_OK)

def part(components, component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)