from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
pagesApiBase = "https://api.hubapi.com/cospages/v1/pages"
pagesSlothApiQuery = (f"access_token={accessToken}&subcategory__eq=site_page&limit=1000")

slothedWebsitePages = requests.get(pagesApiBase, params=pagesSlothApiQuery)
slothedWebsitePageObjects = slothedWebsitePages.json()["objects"]
slothedWebsitePageObjectsCount = len(slothedWebsitePageObjects)
print (f"Hold your butts! Moving {slothedWebsitePageObjectsCount} website pages to landing pages :butt-holdings:")

for slothedWebsitePageObject in slothedWebsitePageObjects:
    slothedPageId = slothedWebsitePageObject["id"]
    wpTpLpUri = (f"{pagesApiBase}/{slothedPageId}?access_token={accessToken}")
    wpTpLpPayload = {"subcategory": "landing_page"}
    movePageRequest = requests.put(wpTpLpUri, json=wpTpLpPayload)
    if movePageRequest.status_code == 200:
        print (f"Moved page {slothedPageId} to Landing Pages")
    else:
        print (f"Failed to move page {slothedPageId} to Landing Pages")
    sleep(.33)