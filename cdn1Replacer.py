import requests
import json
import re
import sys

accessToken = sys.argv[1]
contentGroupId = sys.argv[2]

apiBase = "https://api.hubapi.com/"
listBlogPostsApi = "blogs/v3/blog-posts"
listBlogPostsApiQueryString = (f"access_token={accessToken}&contentGroupId={contentGroupId}&property=id&property=postBody&limit=300")
filePostUrl = (f"{apiBase}filemanager/api/v2/files/download-from-url?access_token={accessToken}")
blogsGetPosts = (f"{apiBase}/{listBlogPostsApi}")
replacers = {}

def findCdn1Uri(postBody):
    imgFinderPattern = re.compile(r'(?<=<img src=").*?(?=")')
    images = re.findall(imgFinderPattern, postBody)
    for image in images:
        if "cdn1" not in image:
            images = images.remove(image)
    return images

def createFmAsset(imgSrc):
    filePostPayload = {"url":imgSrc}
    fileObject = requests.post(filePostUrl, json=filePostPayload)
    cdn2FileUrl = fileObject.json()["url"]
    return cdn2FileUrl

def replaceAllCdn1Uri(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def updatePostBody(postBodyPayload, postId):
    postUpdateUrl = (f"{apiBase}blogs/v3/blog-posts/{postId}?access_token={accessToken}")
    postUpdatePayload = {"postBody":postBodyPayload}
    requests.put(postUpdateUrl, json=postUpdatePayload)

blogSearchObject = requests.get(blogsGetPosts, params=listBlogPostsApiQueryString)
posts = blogSearchObject.json()["objects"]

for post in posts:
    replacers = {}
    postId = post["id"]
    postBody = post["postBody"]
    cdn1sToreplace = findCdn1Uri(postBody)
    if cdn1sToreplace is not None:
        for cdn1Uri in cdn1sToreplace:
            cdn2CreatedAssetUri =  createFmAsset(cdn1Uri)
            replacers[cdn1Uri] = cdn2CreatedAssetUri
            replacedPostBody = replaceAllCdn1Uri(postBody, replacers)
            updatePostBody(replacedPostBody, postId)
        print (f"Replaced cdn1 images in post {postId}")
    else:
        print (f"Found no cdn1 images to replace in post {postId}")