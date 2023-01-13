from cgi import parse_header
from typing import List
from urllib import response
from rest_framework.decorators import api_view
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import os
from backend.notion_api_parser import * 
import requests
from backend.notion_api_parser import * 
from threading import Thread


dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')
components = dict()
list_of_text_data = dict()

NOTION_PAGE_URL = 'https://api.notion.com/v1/blocks/{blockid}/children'
NOTION_PAGE = 'https://api.notion.com/v1/blocks/{blockid}'
NOTION_HEADER = {'Notion-Version': version, 'Authorization': token}

#About CommIT
WHAT_IS_COMMIT = '143e3c801f274f1baf490a25ce2f955a'
WHAT_DOES_COMMIT_DO = '69ad9a1221cf4eabab2497384ae22309'
HOW_TO_APPLY = '3c187de7dd60412eb34249ae026993be'

#Registration Procedure and Place
HOW_TO_REGISTER = '930611ea4fbd4bbb9792bb11e1b17720'
WORKSHOP_GUARANTEED = 'b07937e1b8624b849b5285a33ec250c5'
PAY_DEPOSIT = 'fb45f5af727e4e0588cd4028b44cd244'
GET_TO_SECRETARIAT = '0637ab6dcf9c4bf78827faccdf642b60'

#About the Workshops
WORKSHOP_COST = 'e8dfc4a05a334dd5bcacd567fa9b689c'
BRING_LAPTOP = 'c397c2dcfd1341e2906cf727feeaf2f3'
USE_OWN_LAPTOP = 'bdd21020119a476a8b04e1f8c10770ef'
WORKSHOP_VACANCY = 'fbc2bd751280401b87da69c7e047cc6d'
WHEN_AND_WHERE = 'ad7699f05dbb4239add6754678d3440c'
HOW_LONG = '350bac505483427aaafafdd7763986db'

#Issues regarding Payment of Refundable Deposit
REFUND_IF_CANNOT_ATTEND = 'bcb7192cb1ad4cc3b3737dfe188de596'
WHAT_TO_DO_IF_CANNOT_COME_TO_PAY = 'd5c09d71d0484628ac92c97099441911'
 
#Trainers and Materials Coverage
TRAINERS = 'c4fb2a70a88c4046b2d2b7c36a851b99'
PREREQUISITE = '012a7ec1001245068b863564e58a03b8'
PEOPLE_WITH_BASICS = '74e4214c4258407aa5d9aae8da618932'


# Create your views here.

@api_view(['Get'])
def faq(request):
    data = []
    
    thread = [Thread(target=component, args=("About CommIT", 
    {"what is commit" : WHAT_IS_COMMIT, "what does commit do" : WHAT_DOES_COMMIT_DO, 
     "how to apply": HOW_TO_APPLY})),
    Thread(target=component, args=("Registration Procedure and Place", 
    {"How do I register?": HOW_TO_REGISTER, "workshop place guaranteed": WORKSHOP_GUARANTEED, 
    "When and how do I pay the $5 refundable deposit?": PAY_DEPOSIT,
    "get to secretariat" : GET_TO_SECRETARIAT})),
    Thread(target=component, args = ("About the Workshops",
    {"workshop cost" : WORKSHOP_COST, "bring laptop": BRING_LAPTOP, 
    "use own laptop" : USE_OWN_LAPTOP, "vacancy": WORKSHOP_VACANCY, 
    "time & place": WHEN_AND_WHERE, "how long": HOW_LONG})),
    Thread(target=component, args=("Issues regarding Payment of Refundable Deposit",
    {"get refund if cannot attend": REFUND_IF_CANNOT_ATTEND, "payment": WHAT_TO_DO_IF_CANNOT_COME_TO_PAY})),
    Thread(target=component, args=("Trainers and Materials Coverage",
    {"trainers": TRAINERS, "prerequisite": PREREQUISITE, "basics": PEOPLE_WITH_BASICS}))]
    

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    sort_order = ["About CommIT", "Registration Procedure and Place", "About the Workshops",
    "Issues regarding Payment of Refundable Deposit", "Trainers and Materials Coverage"]
    
    res = {k: list_of_text_data[k] for k in sort_order}
    return Response(res, status=status.HTTP_200_OK)


def part(component, id):
    
    url = NOTION_PAGE_URL.format(blockid = id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    components[component] = parse(data)


def component(header, blockid_list):
    threads = []
    result = []
    
    for i in blockid_list.keys():
        threads.append(Thread(target=part, args=(i, blockid_list[i])))
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    for i in blockid_list.keys():
        result += components[i]
    
    list_of_text_data[header] = result


    


    





