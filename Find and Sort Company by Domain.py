import os, requests, json
import time

def main(event):
  
  token = os.getenv("RevOps")
  domain = event.get("inputFields").get("domain")
  url = "https://api.hubapi.com/crm/v3/objects/companies/search"
  pid = 0
  sid = 0
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
  }
  data = {
    "filterGroups": [
      {
        "filters": [
          {
            "propertyName": "domain",
            "operator": "EQ",
            "value": domain
          }
        ]
      }
    ],
    "properties": ["notes_last_updated", "createdate"],
    "limit": 2,
    "sorts": [
        {
            "propertyName": "notes_last_updated",
            "direction": "DESCENDING"
        }
    ]
  }
  
  time.sleep(1)
  
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  if response.status_code == 200:
    total = (response.json())['total']
    if total > 1:
      response_data = response.json()
      results = response_data.get("results", [])
      with_notes_last_updated = [r for r in results if r.get("properties", {}).get("notes_last_updated")]
      without_notes_last_updated = [r for r in results if not r.get("properties", {}).get("notes_last_updated")]
      without_notes_last_updated.sort(key=lambda r: r.get("properties", {}).get("createdate"), reverse=True)
      sorted_results = with_notes_last_updated + without_notes_last_updated
      ids = []
      for record in sorted_results:
        ids.append(record['id'])
      pid = ids[0]
      sid = ids[1]
    else:
      total = (response.json())['total']
      pid = 0
      sid = 0
  else:
    print(f"Error: {response.status_code}, {response.text}")
  
  return {
    "outputFields": {
      "total": total,
      "primaryId": pid,
      "secondaryId": sid
    }
  }