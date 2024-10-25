import os, requests, json
import time

def main(event):
  token = os.getenv("RevOps")
  pId = event.get("inputFields").get("pId")
  sId = event.get("inputFields").get("sId")
  
  url = "https://api.hubapi.com/crm/v3/objects/companies/merge"
  
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
  }
  
  data = {
    "primaryObjectId": pId,
    "objectIdToMerge": sId
  }
  
  time.sleep(1)
  
  response = requests.post(url, headers=headers, json=data)