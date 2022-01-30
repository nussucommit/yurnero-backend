from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

# DECLARATIONS GO HERE

# Notion URLs
NOTION_DATABASE_URL = "https://api.notion.com/v1/databases"
GET_PAGE_URL = "https://api.notion.com/v1/pages/"
GET_BLOCK_URL = "https://api.notion.com/v1/blocks/"

# request header to access Notion database
TOKEN = "secret_TcMjQSB7rYBBwB6pzhlq5OgR6cRgVwo0oT0h2zIgf1F"
NOTION_VERSION = "2021-08-16"
NOTION_HEADERS = {
  'Authorization': 'Bearer ' + TOKEN,
  'Notion-Version': NOTION_VERSION
}

# PUT VIEWS BELOW

# sample get request
@api_view(['GET'])
def get_notion_database(request):
  response = requests.get(NOTION_DATABASE_URL, headers=NOTION_HEADERS)

  return Response(response.json(), status=status.HTTP_200_OK)

# sample test request: page
@api_view(['GET'])
def get_sample_page(request):
  page_id = "b568ee3e563a48b4a1a865aee9ecb6ce"
  url = GET_PAGE_URL + page_id
  response = requests.get(url, headers=NOTION_HEADERS)

  return Response(response.json(), status=status.HTTP_200_OK)

# sample test request: block
@api_view(['GET'])
def get_sample_block(request):
  block_id = "874fb138423a464fb6b45f82ec38dc36"
  url = GET_BLOCK_URL + block_id
  response = requests.get(url, headers=NOTION_HEADERS)

  return Response(response.json(), status=status.HTTP_200_OK)
