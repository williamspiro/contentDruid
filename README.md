# contentDruid
A collection of Python scripts for various content object jobs. These are very powerful scripts, so please read the spec and use them with respect and ease. A _sloth_ is is a passive script, finding things for you. A _load_ requires some sort of input file. 
p.s. I like to call [Python](https://www.python.org/) scripts, "Python pythons." Why? Because it is fun :)  
Eveything is written in __Python 3.6.5__ with 3.X in mind  

__filesSlothRestore__ - Find and restore deleted file objects   
__urlMappingLoad__ - Bulk edit and create URL mapping objects   
__cmsFinder__ - Figures out which CMS a page uses  
__blogFeaturedImageSoup__ - Soup featured images from an external blog, upload them to the File Manager, set them as featured for the posts respective HubSpot equivalent  
__filesDeleteLoad__ - Deletes file objects by id  

## filesSlothRestore
A Python python to find deleted file objects and restore them  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes two agruments: `accessToken` & `slothStart`  
`accessToken` - An access_token for the portal you want to filesSlothRestore  
`slothStart` - A millisecond unix timestamp used in the `deleted_at__gt` request parameter to dictate the start time of file deletion timestamps to GET  

```
$ python3 filesSlothRestore.py 1234-5678-9123-4567 1529816400000  
```
Runs `filesSlothRestore.py` finding files deleted after 1529816400000 (June 24th, 2018 0:00:00) for portal with access token `1234-5678-9123-4567`  

## urlMappingLoad
A Python python to bulk edit and create URL mapping objects  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes one agrument: `accessToken`    
`accessToken` - An access_token for the portal you want to urlMappingLoad  
This Python python also requires a JSON file to import. This file should be called `mappingsToLoad.json` and should live in the "import" folder - path `import/mappingsToLoad.json`.  This file should have a JSON object with the updated JSON of the mappings you wish to update, and that of new mappings to create, like:
```
[
    {  
        "id":5265745360,
        "destination":"https://www.destination.com",
        "redirectStyle":301
    },
    {  
        "id":4967273182,
        "isMatchFullUrl": true,
        "isProtocolAgnostic": false
    },
    {  
        "routePrefix":"https://www.routeprefix.com/prefix",
        "destination":"https://www.destination.com/destination",
        "isOnlyAfterNotFound":true,
        "redirectStyle":301,
        "precedence":123,
        "isPattern": false,
        "isMatchQueryString": true
    }
]
```
Only the included JSON keys will be updated for a given mapping id included in `mappingsToLoad.json` (first 2 examples). Mapping objects in `mappingsToLoad.json` without an `id` key will be created as new mappings (3rd example). 

```
$ python3 urlMappingLoad.py 1234-5678-9123-4567  
```
Runs `urlMappingLoad.py` on portal with access token `1234-5678-9123-4567`, updating each mapping id included in `mappingsToLoad.json` with the included keys in in the first two individual mapping JSON objects, and creating a new mapping with included keys for the third

## cmsFinder
_REQUIRES_  
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  

_USAGE_  
This Python python figures out which CMS a page uses. Requyires creating a Python list in `pagesToScrub` of the pages/sites to crawl, like: `pagesToScrub = ["http://www.puppy.com", "http://cats.com", ...]` 
```
$ python3 cmsFinder.py
```
This will output the CMS a site uses based on the `meta name="generator"` HTML tag. If there is no `generator` meta tag, we will look for some other common signs of certain CMSs.


## blogFeaturedImageSoup
A Python python to find the featured image on an external blog, upload it to the HubSpot File Manager, and then set the HubSpot hosted version of the posts' `featuredImage` with the newly uploaded File Manager asset  
_REQUIRES_  
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python requires manually setting 4 variables: `accessToken`, `blogRootUrl`, `featuredImageSelector` & `postsToSoupScrubKitten`

`accessToken` - An access_token for the portal you want to blogFeaturedImageSoup  
`blogRootUrl`- The external blogs root url 
`featuredImageSelector` - The CSS selector which select the external blogs featured image (ex. `.featured-image img`)  
`postsToSoupScrubKitten` - A python list of the slugs of all of the external posts to soup (ex. `["slug/post/1", "slug/post/2", "slug/post/3"]`)  

It is important that the post slugs of the external and HubSpot posts are the same. `blogRootUrl` + `postsToSoupScrubKitten[slugs]` should equal the actual URL of the posts. `slug`s should not start with a `/`, rather, `blogRootUrl` should end with a `/`

```
$ python3 blogFeaturedImageSoup.py
```

## filesDeleteLoad.py
DELETES file objects by id  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes one agrument: `accessToken`    
`accessToken` - An access_token for the portal you want to filesDeleteLoad  

It also requires a Python list of file object ids to delete, set in the `filesToDelete` variable, like: `filesToDelete = [1234, 5678, 3658, 8573]`  

```
$ python3 filesDeleteLoad.py 1234-5678-9123-4567
```
Runs `filesDeleteLoad.py` on portal with access token `1234-5678-9123-4567`, DELETING every file object id in the `filesToDelete` variable