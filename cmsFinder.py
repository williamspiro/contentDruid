from bs4 import BeautifulSoup
import urllib2
from urllib2 import URLError, HTTPError

pagesToScrub = ["http://advantagedistributors.com", "http://abidonetwork.com"]

for pageToScrub in pagesToScrub:
    try:
        page = urllib2.urlopen(pageToScrub)
    except HTTPError as e:
        print "hmmm, I had a hard time fetching {}".format(pageToScrub)
    except URLError as e:
        print "hmmm, I had a hard time fetching {}".format(pageToScrub)
    else:
        soup = BeautifulSoup(page, "html.parser")
        if soup.find(attrs={"name":"generator"}):
            cmsMeta = soup.find(attrs={"name":"generator"})
            cms = cmsMeta.get("content")
            print "{} uses the cms {}".format(pageToScrub, cms)
        else:
            print "hmmm, I was not able to figure out which cms {} uses".format(pageToScrub)
