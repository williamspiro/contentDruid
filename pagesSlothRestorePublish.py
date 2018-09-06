from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
pagesApiBase = "https://api.hubapi.com/content/api/v4/pages"
pagesSlothApiQuery = (f"access_token={accessToken}&includeDeleted=true&deletedAt__gt={slothStart}&limit=1000")

slothedPages = requests.get(pagesApiBase, params=pagesSlothApiQuery)
slothedPageObjects = slothedPages.json()["objects"]
deletedPagesIdsCount = len(slothedPageObjects)
print (f"Hold your butts! Restoring {deletedPagesIdsCount} pages :butt-holdings:")

for slothedPageObject in slothedPageObjects:
    slothedPageId = slothedPageObject["id"]
    slothedDeletedBy = slothedPageObject["deletedBy"]
    slothedstate_when_deleted = slothedPageObject["meta"]["state_when_deleted"]
    if slothedDeletedBy == "SCOPE_CHANGE" and slothedstate_when_deleted == "PUBLISHED_OR_SCHEDULED":
        pageApiRestore = (f"{pagesApiBase}/{slothedPageId}/restore-deleted?access_token={accessToken}")
        restorePage = requests.put(pageApiRestore)
        if restorePage.status_code == 200:
            pageRestoreRequestUri = (f"{pagesApiBase}/{slothedPageId}/publish-action?access_token={accessToken}")
            publishPagePayload = {'action': 'schedule-publish'}
            publishedPage = requests.post(pageRestoreRequestUri, json=publishPagePayload)
            if publishedPage.status_code == 204:
                print (f"Restored and published page id {slothedPageId}")
            else:
                print (f"Failed to publish page id {slothedPageId}, but it was restored")
        else:
            print (f"Hmmm, something went wrong resoring page id {slothedPageId}")
    elif slothedDeletedBy == "SCOPE_CHANGE":
        pageApiRestore = (f"{pagesApiBase}/{slothedPageId}/restore-deleted?access_token={accessToken}")
        restorePage = requests.put(pageApiRestore)
        if restorePage.status_code == 200:
            print (f"Restored page id {slothedPageId}, but did not publish it as it was not PUBLISHED_OR_SCHEDULED when deleted")
        else: 
            print (f"Hmmm, something went wrong resoring page id {slothedPageId}")
    else: 
        print (f"Found deleted page {slothedPageId}, but it was not deleted by SCOPE_CHANGE")
    sleep(.33)