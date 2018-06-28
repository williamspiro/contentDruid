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
            html = page.read()
            if b"wp-content" or b"wordpress" or b"wp-json" in html:
                cms = ("Wordpress")
            elif b"static.wixstatic.com" or b"wix" in html:
                cms = ("Wix")
            elif b"static1.squarespace.com" or b"squarespace" in html:
                cms = ("Squarespace")
            elif b"weebly" in html:
                cms = ("Weebly")
            elif b"drupal" in html:
                cms = ("Drupal")
            elif b"craftCMS" or b"CRAFT" in html:
                cms = ("CRAFT")
            else:
                cms = ("unknown")
    psiGradableUri = pageToScrub.split("//")[1]
    psiDeskReqUri = (f"{psiBaseApi}{psiGradableUri}&fields=id%2CruleGroups")
    psiMobReqUri = (f"{psiBaseApi}{psiGradableUri}&fields=id%2CruleGroups&strategy=mobile")
    deskPsiGrade = psiGrade(psiDeskReqUri)
    mobPsiGrade = psiGrade(psiMobReqUri)

    print (f"{pageToScrub}, {cms}, {deskPsiGrade}, {mobPsiGrade}")



