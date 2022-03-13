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


NOTION_PAGE_URL = 'https://api.notion.com/v1/blocks/{blockid}/children'
NOTION_HEADER = {'Notion-Version': version, 'Authorization': token, 
'Content-Type': 'application/json', 'Accept': 'application/json'}
FEEDBACK_DATABASE_ID = "df61518678a84bfbbdda34e6f253af69"


@api_view(['Post'])
def feedback(request):
    content = json.loads(str(request.body, encoding='utf-8'))
    try:
        data = configure_json(content['name'], content['email'], content['subject'], content['message'])
        response = requests.post("https://api.notion.com/v1/pages", headers=NOTION_HEADER,data=json.dumps(data))
        return Response(response.json(), status=status.HTTP_201_CREATED) 
    except:
        return Response({"invalid": "certain values are missing"}, status=status.HTTP_400_BAD_REQUEST)


def configure_json(name, email, subject, message):
    feedback_skeleton = {
        "parent": {
            "database_id": FEEDBACK_DATABASE_ID
        },
        "properties": {
            "Full Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "Email address": {
                "email": email
            },
            "Subject" : {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": subject
                        }
                    }
                ]
            },
            "Message" : {
                "rich_text": [
                    {
                    "type": "text",
                    "text": {
                        "content": message
                        }
                    }
                ]
            }
        }
    }

    return feedback_skeleton