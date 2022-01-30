from numpy import extract
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests

from dotenv import load_dotenv 
import os 
from pathlib import Path 
 
dotenv_path = Path('backend/.env') 
load_dotenv(dotenv_path) 
token = os.getenv('token') 
version = os.getenv('version')
headers = {
  'Authorization': 'Bearer ' + token,
  'Notion-Version': version
}

# Create your views here.


@api_view(['GET'])
def get_creation(request):
    url = 'https://api.notion.com/v1/blocks/2aa850b21f7e4d9f846f61dc78c6f145/children'
    response = requests.get(url, headers=headers)
    data = response.json()
    result = parse_response(data)
    return JsonResponse({"data": result})

def parse_response(data):
    result = []
    ids = extract_id(data)
    titles = extract_title(data)
    for id, title in zip(ids, titles):
        content = extract_content(id)
        result.append({"title": title, "content": content})
    return result

def extract_id(results):
    ids = []
    for result in results["results"]:
        id = result["id"].replace("-", "")
        ids.append(id)
    return ids

def extract_title(results):
    titles = []
    for result in results["results"]:
        if (not "child_page" in result):
            titles.append("")
            continue
        title = result["child_page"]["title"]
        titles.append(title)
    return titles

def extract_content(id):
    result = ""
    url = 'https://api.notion.com/v1/blocks/' + id + '/children'
    response = requests.get(url, headers=headers)
    data = response.json()
    for content in data["results"]:
        if (not content):
            continue
        else:
            type = content["type"]
            if (type == "paragraph"): 
                for text in (content["paragraph"]["text"]):
                    result = result + (text["text"]["content"])
            elif (type == "image"):
                type = content["image"]["type"]
                result = content["image"][type]["url"] + "\n"
    return result