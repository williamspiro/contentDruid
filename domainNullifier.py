from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
domain = sys.argv[2]
apiBase = (f"https://api.hubapi.com/cospages/v1/pages")
pagesSlothApiQuery = (f"access_token={accessToken}&limit=1000&property=id&property=domain&domain={domain}")

slothedPages = requests.get(apiBase, params=pagesSlothApiQuery)
slothedPageObjects = slothedPages.json()["objects"]

for slothedPageObject in slothedPageObjects:
    slothedPageId = slothedPageObject["id"]
    slothedPageDomain = slothedPageObject["domain"]
    if slothedPageDomain == domain:
        print (f"Page ID {slothedPageId} has a specified domain key of {domain}, attempting to clear now")
        pageDomainNullifyUri = (f"{apiBase}/{slothedPageId}?access_token={accessToken}")
        pageDomainNullifyPayload = {'domain': ''}
        pageDomainNullifyPage = requests.put(pageDomainNullifyUri, json=pageDomainNullifyPayload)
        if pageDomainNullifyPage.status_code == 200:
            print (f"Nullified domain of {slothedPageId}")
        else:
            print (f"Failed to nullify domain of {slothedPageId}")
        sleep(.33)
