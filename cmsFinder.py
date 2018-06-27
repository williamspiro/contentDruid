from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

pagesToScrub = ["http://advantagedistributors.com", "http://abidonetwork.com/", "http://www.thefriendlydeveloper.com", "http://aggio.io", "https://3dfortify.com", "https://www.aacustomsbroker.com/"]

for pageToScrub in pagesToScrub:
    try:
        page = urlopen(pageToScrub)
    except HTTPError as e:
        print (f"hmmm, I had a hard time fetching {pageToScrub}")
    except URLError as e:
        print (f"hmmm, I had a hard time fetching {pageToScrub}")
    else:
        soup = BeautifulSoup(page, "html.parser")
        if soup.find(attrs={"name":"generator"}):
            cmsMeta = soup.find(attrs={"name":"generator"})
            cms = cmsMeta.get("content")
            print (f"{pageToScrub} uses the cms {cms}")
        else:
            html = page.read()
            if "wp-content" in html:
                print (f"{pageToScrub} uses the cms Wordpress")
            elif "static.wixstatic.com" in html:
                print (f"{pageToScrub} uses the cms Wix")
            elif "static1.squarespace.com" in html:
                print (f"{pageToScrub} uses the cms Squarespace")
            else:
                print (f"hmmm, I was not able to figure out which cms {pageToScrub} uses")