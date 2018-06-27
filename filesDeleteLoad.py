from time import sleep
import requests
import sys

accessToken = sys.argv[1]
filesApiBase = (f"https://api.hubapi.com/filemanager/api/v2/files")

filesToDelete = [1234, 5678, 3658, 8573]

for fileToDelete in filesToDelete:
    deleteRequestUri = (f"{filesApiBase}/{fileToDelete}?access_token={accessToken}")
    deletedFileObject = requests.delete(deleteRequestUri)
    if deletedFileObject.status_code == 200:
        print (f"Deleted file id {fileToDelete}")
    else:
        print (f"Hmmm, something went wrong deleting file id {fileToDelete}. The error was {deletedFileObject.text}")
    sleep(.4)