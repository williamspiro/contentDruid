from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
contentGroupId = sys.argv[3]
targetDeletedBy = sys.argv[4]
postsApiBase = "https://api.hubapi.com/blogs/v3/blog-posts"
postsSlothApiQuery = (f"access_token={accessToken}&includeDeleted=true&deletedAt__gt={slothStart}&limit=1000&content_group_id={contentGroupId}")

slothedPosts = requests.get(postsApiBase, params=postsSlothApiQuery)
slothedPostObjects = slothedPosts.json()["objects"]
deletedPostsIdsCount = len(slothedPostObjects)
print (f"Hold your butts! Restoring {deletedPostsIdsCount} posts :butt-holdings:")

for slothedPostObject in slothedPostObjects:
    slothedPostId = slothedPostObject["id"]
    slothedDeletedBy = slothedPostObject["deletedBy"]
    slothedstate_when_deleted = slothedPostObject["meta"]["state_when_deleted"]
    postApiRestore = (f"{postsApiBase}/{slothedPostId}/restore-deleted?access_token={accessToken}")
    if slothedDeletedBy == targetDeletedBy and slothedstate_when_deleted == "PUBLISHED":
        restorePost = requests.put(postApiRestore)
        if restorePost.status_code == 200:
            postRestoreRequestUri = (f"{postsApiBase}/{slothedPostId}/publish-action?access_token={accessToken}")
            publishPostPayload = {'action': 'schedule-publish'}
            publishedPost = requests.post(postRestoreRequestUri, json=publishPostPayload)
            if publishedPost.status_code == 204:
                print (f"Restored and published post id {slothedPostId}")
            else:
                print (f"Failed to publish post id {slothedPostId}, but it was restored. publish failed with {publishedPost.status_code}")
        else:
            print (f"Hmmm, something went wrong resoring post id {slothedPostId}")
    elif slothedstate_when_deleted != "PUBLISHED":
        restorePost = requests.put(postApiRestore)
        if restorePost.status_code == 200:
            print (f"Restored post id {slothedPostId}, but did not publish it as it was not PUBLISHED when deleted (it was {slothedstate_when_deleted})")
        else: 
            print (f"Hmmm, something went wrong restoring post id {slothedPostId}. {restorePost.url}, {restorePost.status_code}")
    else: 
        print (f"Found deleted post {slothedPostId}, but it was not deleted by {targetDeletedBy} (it was deleted by {slothedDeletedBy})")
    sleep(.33)