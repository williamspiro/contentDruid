from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
oldAuthorId = sys.argv[2]
contentGroupId = sys.argv[3]
newAuthorId = sys.argv[4]

payload= {"blogAuthorId": newAuthorId }

def errorCheck(updateAuthors, onePost):
    if updateAuthors == "200":
        print(f"updated post {onePost}")
    else:
        print(f"could not update post {onePost}")

def postsAuthorSet(accessToken, oldAuthorId, contentGroupId, newAuthorId):
    postsApiBase = "https://api.hubapi.com/blogs/v3/blog-posts"
    postsAuthorApiQuery = (f"access_token={accessToken}&limit=300&blog_author_id={oldAuthorId}&contentGroupId={contentGroupId}&property=name&property=blogAuthorId&property=id")
    originalPosts = requests.get(postsApiBase, params=postsAuthorApiQuery).json()
    totalPosts = originalPosts["total"]
    runMode = input(f"Found {totalPosts} posts. Would you like to run in safe mode, or make changes? To run in safe mode, type SAFE. To make changes, type BOOM: ")
    if runMode == "SAFE":
        if totalPosts <= 300:
            print("Running in SAFE mode. Less than 300 posts. No offset needed.")
            for postObject in originalPosts["objects"]:
                onePost = str(postObject["id"])
                print(f"Would update post id {onePost} to have author {newAuthorId}. This is an example.")
                break
        else:
            print("Running in SAFE mode. More than 300 posts. Running multiple times with offset.")
            totalLoops = totalPosts/300
            loopIndex = 0
            while loopIndex <= totalLoops:
                offset = int(loopIndex * 300)
                print("Running with an offset of", offset, "on loop index", loopIndex)
                postsManyPosts = (f"access_token={accessToken}&limit=300&blog_author_id={oldAuthorId}&contentGroupId={contentGroupId}&property=name&property=blogAuthorId&property=id&offset={offset}")
                manyPosts = originalPosts = requests.get(postsApiBase, params=postsManyPosts).json()
                for postObject in manyPosts["objects"]:
                    onePost = str(postObject["id"])
                    print(f"Would update post id {onePost} to have author {newAuthorId}. This is an example.")
                    break
                loopIndex += 1 
                break
    elif runMode == "BOOM":
        if totalPosts <= 300:
            print("Making changes on less than 300 posts. No offset needed.")
            for postObject in originalPosts["objects"]:
                onePost = str(postObject["id"])
                authorsRequest= (f"{postsApiBase}/{onePost}?access_token={accessToken}")
                updateAuthors = requests.put(authorsRequest, json=payload)
                errorCheck(updateAuthors, onePost)
        else:
            print("Making changes on more than 300 posts. Running multiple times with offset.")
            totalLoops = totalPosts/300
            loopIndex = 0
            while loopIndex <= totalLoops:
                offset = int(loopIndex * 300)
                print("Running with an offset of", offset, "on loop index", loopIndex)
                postsManyPosts = (f"access_token={accessToken}&limit=300&blog_author_id={oldAuthorId}&contentGroupId={contentGroupId}&property=name&property=blogAuthorId&property=id&offset={offset}")
                manyPosts = originalPosts = requests.get(postsApiBase, params=postsManyPosts).json()
                for postObject in manyPosts["objects"]:
                    onePost = str(postObject["id"])
                    authorsRequest= (f"{postsApiBase}/{onePost}?access_token={accessToken}")
                    updateAuthors = requests.put(authorsRequest, json=payload)
                    errorCheck(updateAuthors, onePost)
                loopIndex += 1 
    else:
        print("Unexpected input. Please run again.")

postsAuthorSet(accessToken,oldAuthorId,contentGroupId,newAuthorId)
