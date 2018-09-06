from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
pagesApiBase = "https://api.hubapi.com/content/api/v4/pages"
pagesSlothApiQuery = (f"access_token={accessToken}&includeDeleted=true&deletedAt__gt={slothStart}&limit=1")

slothedPages = requests.get(pagesApiBase, params=pagesSlothApiQuery)
slothedPageObjects = slothedPages.json()["objects"]
deletedPagesIdsCount = len(slothedPageObjects)
print (f"Hold your butts! Restoring {deletedPagesIdsCount} pages :butt-holdings:")

for slothedPageObject in slothedPageObjects:
    slothedPageId = slothedPageObject["id"]
    pageApiRestore = (f"{pagesApiBase}/{slothedPageId}/restore-deleted?access_token={accessToken}")
    restorePage = requests.put(pageApiRestore)
    if restorePage.status_code == 200:
        print (f"Restored page id {slothedPageId}, trying to publish it now")
        pageRestoreRequestUri = (f"https://api.hubspot.com/cospages/v1/landing-pages/{slothedPageId}/publish-action?access_token={accessToken}")
        publishPagePayload = {'action': 'schedule-publish'}
        restoredPage = requests.post(pageRestoreRequestUri, json=publishPagePayload)
        if restoredPage.status_code == 204:
            print (f"Published page id {slothedPageId}")
        else:
            print (f"Failed to publish page id {slothedPageId}")
    else:
        print (f"Hmmm, something went wrong resoring page id {slothedPageId}")
    sleep(.33)