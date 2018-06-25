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
        editMappingApiRequest = "{}/{}?access_token={}".format(mappingsApiBase, mappingObjectId, accessToken)
        mappingObject = requests.put(editMappingApiRequest, json=mappingObjectJson)
        if mappingObject.status_code == 200:
            print "Updated URL mapping id {}".format(mappingObjectId)
        else:
            print "Hmmm, something went wrong updating URL mapping {}. The error was {}".format(mappingObjectId, mappingObject.text)
    else:
        createMappingApiRequest = "{}?access_token={}".format(mappingsApiBase, accessToken)
        newMappingObject = requests.post(createMappingApiRequest, json=mappingObjectJson)
        if newMappingObject.status_code == 201:
            newMappingPrefix = newMappingObject.json()["routePrefix"]
            newMappingDestination = newMappingObject.json()["destination"]
            print "Wahoo! Created a new mapping with redirect path {} and desitnation {}".format(newMappingPrefix, newMappingDestination)
        else:
            print "Hmmm, something went wrong creating this url mapping. The error was {}".format(newMappingObject.text)
    sleep(.33)