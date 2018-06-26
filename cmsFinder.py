from bs4 import BeautifulSoup
import urllib2

pagesToScrub = ["http://www.puppy.com", "http://cats.com", "http://www.kittens.com"]

for pageToScrub in pagesToScrub:
    page = urllib2.urlopen(pageToScrub)
    soup = BeautifulSoup(page, "html.parser")
    if soup.find(attrs={"name":"generator"}):
        cmsMeta = soup.find(attrs={"name":"generator"})
        cms = cmsMeta.get("content")
        print "{} uses the cms {}".format(pageToScrub, cms)
    else:
        print "hmmm, I was not able to figure out which cms {} uses".format(pageToScrub)
