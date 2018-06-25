from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
slothEnd = sys.argv[3]
filesApiBase = "https://api.hubapi.com/api/v2/files"
filesSlothApiQuery = "access_token={}&include_deleted=true&deleted_at__gt={}&deleted_at__lt={}".format(accessToken, slothStart, slothEnd)

slothedFiles = requests.get(filesApiBase, params=filesSlothApiQuery)
slothedFileObjects = slothedFiles.json()["objects"]
deletedFileIdsCount = len(slothedFileIds)
print "Hold your butts! Restoring {} files :butt-holdings:".format(deletedFileIdsCount) 

for slothedFileObject in slothedFileObjects:
    slothedFileId = slothedFileObject["id"]
    filesApiRestore = "{}/{}/restore-deleted?access_token={}".format(filesApiBase, fileId, accessToken)
    restoreFile = requests.put(filesApiRestore)
    if restoreFile.response_code == 200:
        print "Restored file id {}".format(fileId)
    else:
        print "Hmmm, something wen wrong resoring file id {}".format(fileId)
    sleep(.33)