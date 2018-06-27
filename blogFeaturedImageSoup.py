from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json

accessToken = "1234-5678-9123-456-789"
blogRootUrl = "http://www.blogrooturl.com/"
featuredImageSelector = ".featured-image img"
postsToSoupScrubKitten = ["slug/post/1", "slug/post/2", "slug/post/3"]

queryParams = (f"?access_token={accessToken}")
apiBase = "https://api.hubapi.com/"

for x in postsToSoupScrubKitten:
    slug = (x)
    page = urlopen(blogRootUrl + slug)
    soup = BeautifulSoup(page, "html.parser")
    fi = soup.select(featuredImageSelector)
    fiSource = fi[0]['src']

    filePostUrl = (f"{apiBase}filemanager/api/v2/files/download-from-url{queryParams}")
    filePostPayload = {"url":fiSource}
    fileObject = requests.post(filePostUrl, json=filePostPayload)
    fileUrl = fileObject.json()["url"]
    print (f"Created file URL {fileUrl}")

    blogsGetSearchUrlParams = (f"{queryParams}&slug={slug}&property=slug&property=id")
    blogsGetSearchUrl = (f"{apiBase}/blogs/v3/blog-posts")
    blogSearchObject = requests.get(blogsGetSearchUrl, params=blogsGetSearchUrlParams)
    postIds = blogSearchObject.json()["objects"]
    postId = postIds[0]["id"]
    print (f"Found post id {postId} with slug {slug}")

    pageUpdateUrl = (f"{apiBase}blogs/v3/blog-posts/{postId}{queryParams}")
    pageUpdatePayload = filePostPayload = {"useFeaturedImage":"true", "featuredImage":fileUrl}
    pageObject = requests.put(pageUpdateUrl, json=pageUpdatePayload)
    print (f"Set {fileUrl} as the featuredImage for post id {postId}")