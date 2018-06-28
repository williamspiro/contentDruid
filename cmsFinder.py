from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import requests
import json

pagesToScrub = ["http://www.puppy.com", "http://cats.com", "http://www.kittens.com"]

psiBaseApi = (r"https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=http%3A%2F%2F")
print ("Domain, CMS, Desktop PSI Score, Mobile PSI Score")

def psiGrade (gradeUri):
    psiDataObject = requests.get(gradeUri)
    if psiDataObject.json()["id"]:
        jsonPsiDataObject = psiDataObject.json()["ruleGroups"]
        psiSpeed = jsonPsiDataObject["SPEED"]["score"]
        return (psiSpeed)
    else:
        return ("unknown")

def cmsTextMatch (html):
    if b"static.wixstatic.com" in html or b"wix" in html:
        return ("Wix")
    elif b"wp-content" in html or b"wordpress" in html or b"wp-json" in html: 
        return ("Wordpress")
    elif b"squarespace" in html: # or b"squarespace" in html
        return ("Squarespace")
    elif b"weebly" in html:
        return ("Weebly")
    elif b"drupal" in html:
        return ("Drupal")
    elif b"craftCMS" in html or b"CRAFT" in html:
        return ("CRAFT")
    else:
        return ("unknown")    

for pageToScrub in pagesToScrub:
    cms = ""
    deskPsiGrade = ""
    mobPsiGrade = ""
    try:
        page = urlopen(pageToScrub)
    except HTTPError as e:
        cms = ("unknown")
    except URLError as e:
        cms = ("unknown")
    else:
        soup = BeautifulSoup(page, "html.parser")
        if soup.find(attrs={"name":"generator"}):
            cmsMeta = soup.find(attrs={"name":"generator"})
            cms = cmsMeta.get("content")
        else:
            cms = cmsTextMatch(urlopen(pageToScrub).read())
            
    psiGradableUri = pageToScrub.split("//")[1]
    psiDeskReqUri = (f"{psiBaseApi}{psiGradableUri}&fields=id%2CruleGroups")
    psiMobReqUri = (f"{psiBaseApi}{psiGradableUri}&fields=id%2CruleGroups&strategy=mobile")
    deskPsiGrade = psiGrade(psiDeskReqUri)
    mobPsiGrade = psiGrade(psiMobReqUri)

    print (f"{pageToScrub}, {cms}, {deskPsiGrade}, {mobPsiGrade}")



