from rest_framework.decorators import api_view
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import os
import json
import requests

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')


NOTION_HEADER = {'Notion-Version': version, 'Authorization': token, 
'Content-Type': 'application/json', 'Accept': 'application/json'}
SUBSCRIBE_DATABASE_ID = "6c07d10d4bf9442c935813dbcd7bf780"

@api_view(['Post'])
def subscribe(request):
    content = json.loads(str(request.body, encoding='utf-8'))
    try:
        data = configure_json(content['email'], content['year'], content['name'])
        response = requests.post("https://api.notion.com/v1/pages", headers=NOTION_HEADER,data=json.dumps(data))
        return Response(response.json(), status=status.HTTP_201_CREATED) 
    except:
        return Response({"invalid": "certain values are missing"}, status=status.HTTP_400_BAD_REQUEST)


def configure_json(email, year, name):
    subscribe_skeleton = {
        "parent": {
            "database_id": SUBSCRIBE_DATABASE_ID
        },
        "properties": {
            "Email address": {
                "email": email
            },
            "year": {
                "number": year
            },
            "Name": {
            "title": [
                {
                "text": {
                    "content": name
                }
                }
            ]
            }
        }
    }

    return subscribe_skeleton