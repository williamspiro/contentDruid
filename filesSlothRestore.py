from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
filesApiBase = "https://api.hubapi.com/filemanager/api/v2/files"
filesSlothApiQuery = "access_token={}&include_deleted=true&deleted_at__gt={}&limit=1000".format(accessToken, slothStart)

slothedFiles = requests.get(filesApiBase, params=filesSlothApiQuery)
slothedFileObjects = slothedFiles.json()["objects"]
deletedFileIdsCount = len(slothedFileObjects)
print "Hold your butts! Restoring {} files :butt-holdings:".format(deletedFileIdsCount) 

for slothedFileObject in slothedFileObjects:
    slothedFileId = slothedFileObject["id"]
    filesApiRestore = "{}/{}/restore-deleted?access_token={}".format(filesApiBase, slothedFileId, accessToken)
    restoreFile = requests.post(filesApiRestore)
    if restoreFile.status_code == 200:
        print "Restored file id {}".format(slothedFileId)
    else:
        print "Hmmm, something wen wrong resoring file id {}".format(slothedFileId)
    sleep(.33)