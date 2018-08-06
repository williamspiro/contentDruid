from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
mappingsApiBase = "https://api.hubapi.com/url-mappings/v3/url-mappings"
mappingsSlothApiQuery = (f"access_token={accessToken}&include_deleted=true&deleted_at__gt={slothStart}&limit=1000")

slothedMappings = requests.get(mappingsApiBase, params=mappingsSlothApiQuery)
slothedMappingObjects = slothedMappings.json()["objects"]
deletedMappingIdsCount = len(slothedMappingObjects)
print (f"Hold your butts! Restoring {deletedMappingIdsCount} mappings :butt-holdings:")

for slothedMappingObject in slothedMappingObjects:
    slothedMappingId = slothedMappingObject["id"]
    mappingsApiRestore = (f"{mappingsApiBase}/{slothedMappingId}/restore-deleted?access_token={accessToken}")
    restoreFile = requests.put(mappingsApiRestore)
    if restoreFile.status_code == 200:
        print (f"Restored mapping id {slothedMappingId}")
    else:
        print (f"Hmmm, something went wrong resoring mapping id {slothedMappingId}")
    sleep(.33)