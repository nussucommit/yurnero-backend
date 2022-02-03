import json
from dotenv import load_dotenv
from pathlib import Path
import os
import requests

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')

def parse(data):
    if (data["object"] == "list"):
        return parseList(data["results"])
    

def parseList(data):
    list = []
    for i in data:
        if (i["type"] in ["heading_1", "heading_2", "heading_3"]):
            list.append(parseHeading(i))
        elif (i["type"] == "paragraph"):
            list.append(parseParagraph(i))
        elif (i["type"] == "bulleted_list_item"):
            list.append(parseBulletList(i))
        elif (i["type"] == "table"):
            list.append(parseTable(i))
    return list


def parseHeading(data):
    result = dict()
    result["type"] = "heading"
    result["content"] = data[data["type"]]["text"][0]["plain_text"]
    return result

def parseParagraph(data):
    list = []
    for i in data["paragraph"]["text"]:
        list.append(parseText(i))
    
    result = dict()
    result["type"] = "paragraph"
    result["content"] = list
    return result

def parseText(data):
    result = dict()
    result["type"] = "text"
    result["content"] = data["plain_text"]
    
    special_attribute = dict()
    for attribute in data["annotations"]:
        if (attribute != "color" and data["annotations"][attribute] == True):
            special_attribute[attribute] = True

        elif (attribute == "color" and data["annotations"][attribute] != "default"):
            special_attribute[attribute] = data["annotations"][attribute]
        
        if (data["text"]["link"]):
            special_attribute["link"] = data["text"]["link"]["url"]
    
    result["attribute"] = special_attribute
    return result

def parseBulletList(data):
    result = dict()
    
    result["type"] = "bulleted_list_item"
    list = []
    for i in data["bulleted_list_item"]["text"]:
        bullet_item = parseText(i)
        if data["has_children"]:
            url = 'https://api.notion.com/v1/blocks/' + data["id"] + '/children'
            headers = {'Notion-Version': version, 'Authorization': token}
            response = requests.get(url, headers=headers)
            data = response.json()
            bullet_item["children"] = parse(data)
        
        list.append(bullet_item)
    result["content"] = list
    return result

def parseTable(data):
    result = []
    url = 'https://api.notion.com/v1/blocks/' + data["id"] + '/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    table = response.json()
    for i in table["results"]:
        row = []
        for j in i["table_row"]["cells"]:
            row.append(j[0]["plain_text"])
        result.append(row)
    return {"result": result}


