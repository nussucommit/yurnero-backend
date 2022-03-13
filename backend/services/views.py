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

CENTRE_OVERVIEW_URL = "a48c58b53a3d4286b8dd2c9dfbbc6281"
CENTRE_OPERATINGHOURSE_URL = "6d4a6bbd728743ee8f67ee7a20f5674d"
CENTRE_PRINTINGRATES_URL = "20ff6a061eff4b80b1f08cf9ddc2dbe4"

TRAINING_OVERVIEW_URL = "f02e4f8af490472d952b112e0b22704a"
TRAINING_WORKSHOPREGISTRATION_URL = "f6afd72b4f2149eebbe3622bd5680f4a"
TRAINING_ADOBEPHOTOSHOP_URL = "930ead6d4d124ffa90d3a7e3d4458fd3"
TRAINING_PYTHON_URL = "48c1869d858242bc8287c990afef5518"
TRAINING_MICROSOFTEXCEL_URL = "700cb040f7d14482815b0203296c32e0"
TRAINING_CONTACTUS_URL = "02b1b881b6f24fc3bf48a5f3eb28d345"

EXTERNAL_OVERVIEW_URL = "cb60de72538846a490b990018cc63486"
EXTERNAL_WORKSHOPREGISTRATION_URL = "8f926020d525419aa708e34021d49e84"
EXTERNAL_DATASCIENCE_URL = "57ede608b6b042bea480ee93a966c185"
EXTERNAL_WEBDEV_URL = "0ededa3f0ed440a9a31c7fbdc4c4dbeb"
EXTERNAL_MICROSOFTEXCELVBA_URL = "00481d1cf57041cb8626ba07215ff5aa"

SDP_OVERVIEW_URL = "11075f8948e04d89b61bc16b97b978f7"
SDP_CURRENTAPPLICATIONS_URL = "29b2d08c4eea4a3a95aa0a913a7ec2e0"
SDP_CONTACTUS_URL = "a398833a26f0411aa7f702edd4758203"


# Create your views here.

@api_view(['Get'])
def computercentres(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", CENTRE_OVERVIEW_URL)), 
    Thread(target=part, args=("operatinghours", CENTRE_OPERATINGHOURSE_URL)), 
    Thread(target=part, args=("printingrates", CENTRE_PRINTINGRATES_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["operatinghours"]
    data += components["printingrates"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


@api_view(['Get'])
def trainingworkshops(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", TRAINING_OVERVIEW_URL)), 
    Thread(target=part, args=("workshopregistration", TRAINING_WORKSHOPREGISTRATION_URL)), 
    Thread(target=part, args=("adobephotoshop", TRAINING_ADOBEPHOTOSHOP_URL)),
    Thread(target=part, args=("python", TRAINING_PYTHON_URL)), 
    Thread(target=part, args=("microsoftexcel", TRAINING_MICROSOFTEXCEL_URL)), 
    Thread(target=part, args=("contactus", TRAINING_CONTACTUS_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["workshopregistration"]
    data += components["adobephotoshop"]
    data += components["python"]
    data += components["microsoftexcel"]
    data += components["contactus"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)


@api_view(['Get'])
def externalworkshops(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", EXTERNAL_OVERVIEW_URL)), 
    Thread(target=part, args=("workshopregistration", EXTERNAL_WORKSHOPREGISTRATION_URL)), 
    Thread(target=part, args=("datascience", EXTERNAL_DATASCIENCE_URL)),
    Thread(target=part, args=("webdev", EXTERNAL_WEBDEV_URL)), 
    Thread(target=part, args=("microsoftexcelvba", EXTERNAL_MICROSOFTEXCELVBA_URL))]

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


@api_view(['Get'])
def sdp(request):
    data = []
    
    thread = [Thread(target=part, args=("overview", SDP_OVERVIEW_URL)), 
    Thread(target=part, args=("currentapplications", SDP_CURRENTAPPLICATIONS_URL)), 
    Thread(target=part, args=("contactus", SDP_CONTACTUS_URL))]

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    result = dict()
    data += components["overview"]
    data += components["currentapplications"]
    data += components["contactus"]
    result["result"] = data

    return Response(data, status=status.HTTP_200_OK)



def part(component, id):
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)