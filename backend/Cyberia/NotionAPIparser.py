import json

def parse(data):
    if (data["object"] == "list"):
        return parseList(data["results"])
    

def parseList(data):
    list = []
    for i in data:
        if (i["type"] == "heading_1"):
            list.append(parseHeading(i))
        elif (i["type"] == "paragraph"):
            list.append(parseParagraph(i))
        elif (i["type"] == "bulleted_list_item"):
            list.append(parseBulletList(i))
    return list


def parseHeading(data):
    result = dict()
    result["type"] = "heading"
    result["content"] = data["heading_1"]["text"][0]["plain_text"]
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
            
    
    result["attribute"] = special_attribute
    return result

def parseBulletList(data):
    result = dict()
    
    result["type"] = "bulleted_list_item"
    list = []
    for i in data["bulleted_list_item"]["text"]:
        list.append(parseText(i))
    result["content"] = list
    return result