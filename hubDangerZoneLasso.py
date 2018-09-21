from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
stringToLasso = sys.argv[2]
lassoReplace = sys.argv[3]
mode = sys.argv[4]

pagesApiBase = "https://api.hubapi.com/cospages/v1/pages"
listPagesQueryString = (f"access_token={accessToken}&limit=300")

def lassoString(page, oldString, newString):
    page = page.replace(oldString, newString)
    return page

def updatePage(pageId, revisedJson):
    postUpdateUrl = (f"{pagesApiBase}/{pageId}?access_token={accessToken}")
    updatePageRequest = requests.put(postUpdateUrl, json=json.loads(revisedJson))
    return updatePageRequest

pageObjects = requests.get(pagesApiBase, params=listPagesQueryString)
pages = pageObjects.json()["objects"]
for page in pages:
    pageId = page["id"]
    page = json.dumps(pageObjects.json())
    if stringToLasso in page:
        replacedPage = lassoString(page, stringToLasso, lassoReplace)
        if mode == "write":
            lassoedPage = updatePage(pageId, replacedPage)
            if lassoedPage.status_code == 200:
                print(f"Updated page {pageId} and replaced all instances of {stringToLasso}")
            else:
                print(f"Hmm, something went wrong updating page {pageId}")
        else:
            print(f"READMODE: Found and would have replaced imstances of {stringToLasso} in page {pageId}. New page JSON: {lassoedPage}")
    else:
        print(f"No instances of {stringToLasso} in {pageId}")
    sleep(.33)