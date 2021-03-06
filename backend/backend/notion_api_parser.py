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
        return parse_list(data["results"])
    

def parse_list(data):
    list = []
    for i in data:
        if (i["type"] in ["heading_1", "heading_2", "heading_3"]):
            list.append(parse_heading(i))
        elif (i["type"] == "paragraph"):
            list.append(parse_paragraph(i))
        elif (i["type"] == "bulleted_list_item"):
            list.append(parse_bullet_list(i))
        elif (i["type"] == "table"):
            list.append(parse_table(i))
        elif (i["type"] == "image"):
            list.append(parse_image(i))
    return list


def parse_heading(data):
    result = dict()
    result["type"] = "heading"
    result["content"] = data[data["type"]]["text"][0]["plain_text"]
    return result

def parse_paragraph(data):
    list = []
    for i in data["paragraph"]["text"]:
        list.append(parse_text(i))
    
    result = dict()
    result["type"] = "paragraph"
    result["content"] = list
    return result

def parse_text(data):
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

def parse_bullet_list(data):
    result = dict()
    
    result["type"] = "bulleted_list_item"
    list = []
    for i in data["bulleted_list_item"]["text"]:
        bullet_item = parse_text(i)
        if data["has_children"]:
            url = 'https://api.notion.com/v1/blocks/' + data["id"] + '/children'
            headers = {'Notion-Version': version, 'Authorization': token}
            response = requests.get(url, headers=headers)
            data = response.json()
            bullet_item["children"] = parse(data)
        
        list.append(bullet_item)
    result["content"] = list
    return result

def parse_table(data):
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

def parse_image(data):
    result = dict()
    result["type"] = "image"
    imagetype = data[data["type"]]["type"]
    result["content"] = data[data["type"]][imagetype]["url"]
    return result

