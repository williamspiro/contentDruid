from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
mappingsApiBase = "https://api.hubspot.com/url-mappings/v3/url-mappings"

with open('import/mappingsToUpdate.json') as jsonData:
    mappingData = json.load(jsonData)

for mappingObjectJson in mappingData:
    mappingObjectId = mappingObjectJson["id"]
    del mappingObjectJson["id"]
    mappingApiRequest = "{}/{}?access_token={}".format(mappingsApiBase, mappingObjectId, accessToken)
    mappingObject = requests.put(mappingApiRequest, json=mappingObjectJson)
    if mappingObject.status_code == 200:
        print "Updated URL mapping id {}".format(mappingObjectId)
    else:
        print "Hmmm, something went wrong updating URL mapping {}".format(mappingObjectId)
    sleep(.33)
