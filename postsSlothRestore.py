from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
contentGroupId = sys.argv[3]
postsApiBase = "https://api.hubapi.com/blogs/v3/blog-posts"
postsSlothApiQuery = (f"access_token={accessToken}&include_deleted=true&deleted_at__gt={slothStart}&limit=1000&contentGroupId={contentGroupId}")

slothedPosts = requests.get(postsApiBase, params=postsSlothApiQuery)
slothedPostObjects = slothedPosts.json()["objects"]
deletedPostsIdsCount = len(slothedPostObjects)
print (f"Hold your butts! Restoring {deletedPostsIdsCount} posts :butt-holdings:")

for slothedPostObject in slothedPostObjects:
    slothedPostId = slothedPostObject["id"]
    postsApiRestore = (f"{postsApiBase}/{slothedPostId}/restore-deleted?access_token={accessToken}")
    restorePost = requests.put(postsApiRestore)
    if restorePost.status_code == 200:
        postRestoreRequestUri = (f"{postsApiBase}/{slothedPostId}/publish-action?access_token={accessToken}")
        publishPostPayload = {'action': 'schedule-publish'}
        publishedPost = requests.post(postRestoreRequestUri, json=publishPostPayload)
        if publishedPost.status_code == 204:
            print (f"Restored and published post id {slothedPostId}")
        else:
            print (f"Failed to publish post id {slothedPostId}, but it was restored")
    else:
        print (f"Hmmm, something went wrong resoring post id {slothedPostId}")
    sleep(.33)