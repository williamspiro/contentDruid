from time import sleep
import sys
import requests
import json

# Accept arguments for auth and domain to work
accessToken = sys.argv[1]
domain = sys.argv[2]


# Get all pages on X subdomain 
pageApiBase = "https://api.hubapi.com/cospages/v1/pages"
getPagesQueryString = (f"access_token={accessToken}&limit=2&state__in=PUBLISHED&state__in=PUBLISHED_AB&state__in=PUBLISHED_OR_SCHEDULED&subcategory__eq=site_page")


getSitePages = requests.get(f"{pageApiBase}/list/{domain}", params = getPagesQueryString)
getSitePagesObjects = getSitePages.json()["objects"]

getSitePagesObjectsCount = len(getSitePagesObjects)
print (f"Hold your butts! Unpublishing and archiving {getSitePagesObjectsCount} website pages :butt_holdings:")

# For each page on X subdomain
for sitePageObject in getSitePagesObjects: 
    
   # Save their {slug} and {id}
   slug = sitePageObject["slug"]
   pageId = sitePageObject["id"]

   # Archive and unpublish pages
   arcAndUnpubUrl = (f"{pageApiBase}/archive-and-unpublish?id={pageId}&access_token={accessToken}")
   arcAndUnpubPages = requests.put(arcAndUnpubUrl)
   if arcAndUnpubPages.status_code == 200:
    
        # Append "-archived" to {slug} 
        updateUrlBody = {"slug":f"{slug}-archived"}
        updateUrlRequest = requests.put(f"{pageApiBase}/{pageId}?access_token={accessToken}", json = updateUrlBody)

        if.updateUrlRequest.status_code == 200:
            print(f"Unpublished, archived and updated slug of page {pageId}")
        else:
            print(f"Unpublished and archived page {pageId}, failed to update slug")
    
   else:
       print(f"Failed to unpublish and archive page {pageId}")
   sleep(.33)
