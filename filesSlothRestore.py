from time import sleep
import requests
import json
import sys

accessToken = sys.argv[1]
slothStart = sys.argv[2]
filesApiBase = "https://api.hubapi.com/filemanager/api/v2/files"
filesSlothApiQuery = (f"access_token={accessToken}&include_deleted=true&deleted_at__gt={slothStart}&limit=1000")

slothedFiles = requests.get(filesApiBase, params=filesSlothApiQuery)
slothedFileObjects = slothedFiles.json()["objects"]
deletedFileIdsCount = len(slothedFileObjects)
print (f"Hold your butts! Restoring {deletedFileIdsCount} files :butt-holdings:")

for slothedFileObject in slothedFileObjects:
    slothedFileId = slothedFileObject["id"]
    filesApiRestore = (f"{filesApiBase}/{slothedFileId}/restore-deleted?access_token={accessToken}")
    restoreFile = requests.post(filesApiRestore)
    if restoreFile.status_code == 200:
        print (f"Restored file id {slothedFileId}")
    else:
        print (f"Hmmm, something wen wrong resoring file id {slothedFileId}")
    sleep(.33)