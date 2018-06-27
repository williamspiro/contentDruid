from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
mappingsApiBase = "https://api.hubspot.com/url-mappings/v3/url-mappings"

with open('import/mappingsToLoad.json') as jsonData:
    mappingData = json.load(jsonData)

for mappingObjectJson in mappingData:
    if "id" in mappingObjectJson:
        mappingObjectId = mappingObjectJson["id"]
        del mappingObjectJson["id"]
        editMappingApiRequest = (f"{mappingsApiBase}/{mappingObjectId}?access_token={accessToken}")
        mappingObject = requests.put(editMappingApiRequest, json=mappingObjectJson)
        if mappingObject.status_code == 200:
            print (f"Updated URL mapping id {mappingObjectId}")
        else:
            print (f"Hmmm, something went wrong updating URL mapping {mappingObjectId}. The error was {mappingObject.text}")
    else:
        createMappingApiRequest = "{}?access_token={}".format(mappingsApiBase, accessToken)
        newMappingObject = requests.post(createMappingApiRequest, json=mappingObjectJson)
        if newMappingObject.status_code == 201:
            newMappingPrefix = newMappingObject.json()["routePrefix"]
            newMappingDestination = newMappingObject.json()["destination"]
            print (f"Wahoo! Created a new mapping with redirect path {newMappingPrefix} and desitnation {newMappingDestination}")
        else:
            print (f"Hmmm, something went wrong creating this url mapping. The error was {newMappingObject.text}")
    sleep(.33)