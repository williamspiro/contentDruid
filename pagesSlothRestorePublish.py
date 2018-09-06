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
    if slothedDeletedBy == "SCOPE_CHANGE":
        pageApiRestore = (f"{pagesApiBase}/{slothedPageId}/restore-deleted?access_token={accessToken}")
        restorePage = requests.put(pageApiRestore)
        if restorePage.status_code == 200:
            if slothedstate_when_deleted == "PUBLISHED_OR_SCHEDULED":
                pageRestoreRequestUri = (f"https://api.hubspot.com/cospages/v1/landing-pages/{slothedPageId}/publish-action?access_token={accessToken}")
                publishPagePayload = {'action': 'schedule-publish'}
                restoredPage = requests.post(pageRestoreRequestUri, json=publishPagePayload)
                if restoredPage.status_code == 204:
                    print (f"Restored and published page id {slothedPageId}")
                else:
                    print (f"Failed to publish page id {slothedPageId}")
            else: 
                print (f"Restored page id {slothedPageId}, but did not restore it as it was not PUBLISHED_OR_SCHEDULED when deleted")
        else:
            print (f"Hmmm, something went wrong resoring page id {slothedPageId}")
    else: 
        print ("Found deleted page {slothedPageId}, but it was not deleted by SCOPE_CHANGE")
    sleep(.33)