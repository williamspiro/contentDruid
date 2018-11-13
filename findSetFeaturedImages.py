from time import sleep
import requests
import json
import sys
import re

accessToken = sys.argv[1]
contentGroupId = sys.argv[2]
postsApiBase = "https://api.hubapi.com/blogs/v3/blog-posts"
listPostsQueryString = (f"access_token={accessToken}&limit=100&content_group_id={contentGroupId}&property=id&property=postBody&property=useFeaturedImage&property=featuredImage")

def setFeaturedImage(featuredImageUri, postIdToUpdate):
    postUpdateUrl = (f"{postsApiBase}/{postIdToUpdate}?access_token={accessToken}")
    postUpdatePayload = {"useFeaturedImage":"true", "featuredImage":f"{featuredImageUri}"}
    postUpdateObject = requests.put(postUpdateUrl, json=postUpdatePayload)
    return postUpdateObject

def findPostBodyImage(postBody):
    images = {}
    imgFinderPattern = re.compile(r'(?<=<img src=").*?(?=")')
    images = re.findall(imgFinderPattern, postBody)
    return images

postObjects = requests.get(postsApiBase, params=listPostsQueryString)
posts = postObjects.json()["objects"]

for post in posts:
    postId = post["id"]
    postUseFi = post["useFeaturedImage"]
    postFeaturedImage = post["featuredImage"]
    postBody = post["postBody"]
    if postFeaturedImage == "":
        postBodyFoundImage = findPostBodyImage(postBody)
        if len(postBodyFoundImage) > 0:
            setFeaturedImageRequestObject = setFeaturedImage(postBodyFoundImage[0], postId)
            if setFeaturedImageRequestObject.status_code == 200:
                print(f"Set featured image of post id {postId} to {postBodyFoundImage[0]}")
            else:
                print(f"Failed to set featured image of post id {postId} to {postBodyFoundImage[0]}")
        else:
            print(f"Found no images in post id {postId} to set as featured image")
    elif postFeaturedImage != "" and postUseFi == False:
        setFeaturedImageRequestObject = setFeaturedImage(postFeaturedImage, postId)
        if setFeaturedImageRequestObject.status_code == 200:
            print(f"Enabled featured images for post id {postId} with already set image {postFeaturedImage}")
        else:
            print(f"Failed to enable featured images for post id {postId} with already set image {postFeaturedImage}")
    else:
        print(f"Post id {postId} already has featured images enabled, and is set to {postFeaturedImage}")
    sleep(.2)
    