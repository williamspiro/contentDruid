from time import sleep
import requests
import sys

accessToken = sys.argv[1]

mappingApiBase = "https://api.hubapi.com/url-mappings/v3/url-mappings"
slothedMappings = requests.get(f"{mappingApiBase}?access_token={accessToken}&limit=5000")
slothedMappingsObjects = slothedMappings.json()["objects"]

for mappingToPurge in slothedMappingsObjects:
    mappingToPurgeId = mappingToPurge["id"]
    mappingDeleteRequest = requests.delete(f"{mappingApiBase}/{mappingToPurgeId}?access_token={accessToken}")
    if mappingDeleteRequest.status_code == 204:
        print(f"Deleted mapping id {mappingToPurgeId}")
    else:
        print(f"Failed to delete mapping id {mappingToPurgeId}")
    sleep(.3)