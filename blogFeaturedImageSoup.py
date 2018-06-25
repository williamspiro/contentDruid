from bs4 import BeautifulSoup
import urllib2
import requests
import json

accessToken = "1234-5678-9123-456-789"
blogRootUrl = "http://www.blogrooturl.com/"
featuredImageSelector = ".featured-image img"
postsToSoupScrubKitten = ["slug/post/1", "slug/post/2", "slug/post/3"]

queryParams = "?access_token={}".format(accessToken)
apiBase = "https://api.hubapi.com/"

for x in postsToSoupScrubKitten:
    slug = (x)
    page = urllib2.urlopen(blogRootUrl + slug)
    soup = BeautifulSoup(page, "html.parser")
    fi = soup.select(featuredImageSelector)
    fiSource = fi[0]['src']

    filePostUrl = "{}filemanager/api/v2/files/download-from-url{}".format(apiBase, queryParams)
    filePostPayload = {"name":"blork","url":fiSource}
    fileObject = requests.post(filePostUrl, json=filePostPayload)
    fileUrl = fileObject.json()["url"]
    print "Created file URL {}".format(fileUrl)

    blogsGetSearchUrlParams = "{}&slug={}&property=slug&property=id".format(queryParams, slug)
    blogsGetSearchUrl = "{}/blogs/v3/blog-posts".format(apiBase)
    blogSearchObject = requests.get(blogsGetSearchUrl, params=blogsGetSearchUrlParams)
    postIds = blogSearchObject.json()["objects"]
    postId = postIds[0]["id"]
    print "Found post id {} with slug {}".format(postId, slug)

    pageUpdateUrl = "{}blogs/v3/blog-posts/{}{}".format(apiBase, postId, queryParams)
    pageUpdatePayload = filePostPayload = {"useFeaturedImage":"true", "featuredImage":fileUrl}
    pageObject = requests.put(pageUpdateUrl, json=pageUpdatePayload)
    print "Set {} as the featuredImage for post id {}".format(fileUrl, postId)