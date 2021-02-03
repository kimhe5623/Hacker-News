import requests
import json
import re

ORDERBY = 'order_by'
PAGE = 'page'
POPULAR = 'Popular'
NEW = 'New'
BY_ID = 'by_id'
OBJECT_ID = 'objectID'
ID = 'id'
CHILDREN = 'children'

URL = "https://hn.algolia.com/api/v1/"

def getStories(orderBy, pageNum):
  db = getDB()
  if(db[orderBy]):
    data = list(filter(lambda hit: hit[PAGE] == int(pageNum), db[orderBy]))
    if(data):
      print(f"{data[0]['hits'][0]['title']} => There is in DB")
      return data[0]

  if (orderBy == NEW):
    url = f"{URL}/search_by_date?&tags=story&page={pageNum}"
  elif (orderBy == POPULAR):
    url = f"{URL}/search?tags=story&page={pageNum}"
  rsp = requests.get(url)
  data = json.loads(rsp.text)
  print(f"{data['hits'][0]['title']} => via API")
  db[orderBy].append(data)
  setDB(db)
  
  return data

def getStory(id):
  db = getDB()
  if(db[BY_ID]):
    data = list(filter(lambda hit: int(hit[ID]) == int(id), db[BY_ID]))
    if(data):
      print(f"{data[0]['title']} => There is in DB")
      return data[0]

  url = f"{URL}/items/{id}"
  rsp = requests.get(url)
  data = json.loads(rsp.text)
  for idx in range(len(data[CHILDREN])):
    data[CHILDREN][idx]['text'] = cleanhtml(data[CHILDREN][idx]['text'])
  print(f"{data['title']} => via API")
  db[BY_ID].append(data)
  setDB(db)
  return data

def getDB():
  f = open('db.json')
  data = json.load(f)
  return data

def setDB(data):
  with open('db.json', 'w') as outfile:
    json.dump(data, outfile)

def cleanhtml(raw_html):
  cleaned = ''
  if(raw_html):
    cleaned = raw_html.replace('<p>', '').replace('</p>', '').replace('<i>', '').replace('</i>', '').replace('&#x27;', "'").replace('&#x2F;', '/')
  return cleaned