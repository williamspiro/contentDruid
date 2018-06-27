from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

pagesToScrub = ["http://www.puppy.com", "http://cats.com", "http://www.kittens.com"]

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
            if b"wp-content" or b"wordpress" or b"wp-json" in html:
                print (f"{pageToScrub} uses the cms Wordpress")
            elif b"static.wixstatic.com" or b"wix" in html:
                print (f"{pageToScrub} uses the cms Wix")
            elif b"static1.squarespace.com" or b"squarespace" in html:
                print (f"{pageToScrub} uses the cms Squarespace")
            elif b"weebly" in html:
                print (f"{pageToScrub} uses the cms Weebly")
            elif b"drupal" in html:
                print (f"{pageToScrub} uses the cms Drupal")
            elif b"craftCMS" or b"CRAFT" in html:
                print (f"{pageToScrub} uses the cms Craft")
            else:
                print (f"hmmm, I was not able to figure out which cms {pageToScrub} uses")