from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = int(sys.argv[2])
tagsApiBase = "https://api.hubapi.com/blogs/v3/topics"
tagsSlothApiQuery = (f"access_token={accessToken}&includeDeleted=true&limit=1000")

slothedTags = requests.get(tagsApiBase, params=tagsSlothApiQuery)
slothedTagObjects = slothedTags.json()["objects"]

for slothedTagObject in slothedTagObjects:
    slothedTagId = slothedTagObject["id"]
    slothedTagSlug = slothedTagObject["slug"]
    slothedTagDeletedAt = slothedTagObject["deletedAt"]
    if slothedTagDeletedAt >= slothStart:
        tagsApiRestore = requests.put(f"{tagsApiBase}/{slothedTagId}/restore-deleted?access_token={accessToken}")
        if tagsApiRestore.status_code == 200:
            if "#DEL" in slothedTagSlug:
                tagRevisedSlug = slothedTagSlug.split("#DEL")[0]
                tagSlugUpdatePayload = {"slug":tagRevisedSlug} 
                tagSlugUpdatePayloadRequest = requests.put(f"{tagsApiBase}/{slothedTagId}?access_token={accessToken}", json=tagSlugUpdatePayload)
                if tagsApiRestore.status_code == 200:
                    print (f"Restored tag {slothedTagId} and removed #DEL suffix")
                else:
                    print (f"Restored tag {slothedTagId} but failed to remove #DEL suffix")
            else:
                print (f"Restored tag {slothedTagId}")
        else:
            print (f"Hmmm, something went wrong resoring tag id {slothedTagId}")
        sleep(.33)