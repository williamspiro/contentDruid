# contentDruid
A collection of Python scripts for various content object jobs. These are very powerful scripts, so please read the spec and use them with respect and ease. A _sloth_ is is a passive script, finding things for you. A _load_ requires some sort of input file. 
p.s. I like to call [Python](https://www.python.org/) scripts, "Python pythons." Why? Because it is fun :)  
Eveything is written in __Python 3.6.5__ with 3.X in mind  

__filesSlothRestore.py__ - Find and restore deleted file objects   
__filesDeleteLoad.py__ - Deletes file objects by id  
__urlMappingLoad.py__ - Bulk edit and create URL mapping objects   
__urlMappingSlothRestore.py__ - Find and restore deleted mapping objects   
__postsSlothRestore.py__ - Find and restore deleted post objects  
__findSetFeaturedImages.py__ - Find and set featured images for blog post objects  
__pagesSlothRestorePublish.py__ - Find, restore and publish deleted page objects  
__tagsSlothRestore.py__ - Find and restore deleted tag objects  
__moveWebsiteToLanding.py__ - Move all Website Pages to Landing pages  
__domainNullifier.py__ - Null out the domain field for pages on a certain domain  
__cmsFinder.py__ - Figures out which CMS a page uses and grades it in PSI (desktop and mobile)   
__cdn1Replacer.py__ - Finds cdn1 image src uri in post bodies, and replaces them with newly uploaded cdn2 files  
__hubDangerZoneLasso.py__ - Finds and replaces ALL instances of a string in page objects  

## filesSlothRestore.py
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

## urlMappingLoad.py
A Python python to bulk edit and create URL mapping objects. Regex `(!DEL!).*?[\d]+` is a good way to remove the `!DEL!<some number>` from restored mappings    
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

## urlMappingSlothRestore.py
A Python python to find deleted mappings and restore them. Regex `(!DEL!).*?[\d]+` is a good way to remove the `!DEL!<some number>` from restored mappings     
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes two agruments: `accessToken` & `slothStart`  
`accessToken` - An access_token for the portal you want to urlMappingSlothRestore  
`slothStart` - A millisecond unix timestamp used in the `deleted_at__gt` request parameter to dictate the start time of file deletion timestamps to GET  

```
$ python3 urlMappingSlothRestore.py 1234-5678-9123-4567 1529816400000  
```
Runs `urlMappingSlothRestore.py` finding mappings deleted after 1529816400000 (June 24th, 2018 0:00:00) for portal with access token `1234-5678-9123-4567` 

## postsSlothRestore.py
A Python python to find deleted posts and restore them  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes three agruments: `accessToken`, `slothStart` & `contentGroupId`    
`accessToken` - An access_token for the portal you want to urlMappingSlothRestore  
`slothStart` - A millisecond unix timestamp used in the `deleted_at__gt` request parameter to dictate the start time of file deletion timestamps to GET  
`contentGroupId` - The blog id to find deleted posts in 

```
$ python3 postsSlothRestore.py 1234-5678-9123-4567 1529816400000 2509275571  
```
Runs `postsSlothRestore.py` finding posts deleted after 1529816400000 (June 24th, 2018 0:00:00) for portal with access token `1234-5678-9123-4567` in blog `2509275571`   

## findSetFeaturedImages.py
A Python python which goes through all posts in a blog and enables featured images, finding and setting an image from the post body as featured if one is not already set. If a post has no post body images, nothing will happen to that post.    
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes 2 arguments:  `accessToken` & `contentGroupId`  
`accessToken` - An access_token for the portal you want to findSetFeaturedImages  
`contentGroupId`- The blog id of the blog you want to findSetFeaturedImages  

```
$ python3 findSetFeaturedImages.py sdfgsdfg-5537-sdfgs-bae6-23455 6515379725
```
Loops through all posts in blog id 6515379725 for portal with acces token `sdfgsdfg-5537-sdfgs-bae6-23455`, finding and setting featured images for all posts  

## pagesSlothRestorePublish.py
A Python python to find deleted pages, restore, and publish them  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes two arguments: `accessToken`, `slothStart`  

`accessToken` - An access_token for the portal you want to urlMappingSlothRestore  
`slothStart` - A millisecond unix timestamp used in the `deleted_at__gt` request parameter to dictate the start time of file deletion timestamps to GET  

```
$ python3 pagesSlothRestorePublish.py 1234-5678-9123-4567 1529816400000    
```
Runs `pagesSlothRestorePublish.py` finding pages deleted after 1529816400000 (June 24th, 2018 0:00:00) for portal with access token `1234-5678-9123-4567` and publishes them    

## tagsSlothRestore.py
A Python python to find deleted tag objects and restore them  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes two agruments: `accessToken` & `slothStart`  
`accessToken` - An access_token for the portal you want to tagsSlothRestore  
`slothStart` - A millisecond unix timestamp to dictate tags deleted after X timestamp to be restored  

```
$ python3 tagsSlothRestore.py 1234-5678-9123-4567 1529816400000  
```
Runs `tagsSlothRestore.py` finding tags deleted after 1529816400000 (June 24th, 2018 0:00:00) for portal with access token `1234-5678-9123-4567`  


## moveWebsiteToLanding.py
A Python python to move all Website Pages to Landing Pages  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes one argument: `accessToken`  

`accessToken` - An access_token for the portal you want to moveWebsiteToLanding  

```
$ python3 moveWebsiteToLanding.py 1234-5678-9123-4567  
```
Runs `moveWebsiteToLanding.py` moving all website pages to landing pages for portal with access token `1234-5678-9123-4567`   

## domainNullifier.py
A Python python to null out the domain field for pages on a certain domain. This is helpful to allow pages (ENT portals) to inherit the domain that is primary for their content type. CAREFUL this will null out the domain for every page on a domain, so refine the `pagesSlothApiQuery` if you only want to touch some pages        
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python takes two argument: `accessToken` & `domain`  

`accessToken` - An access_token for the portal you want to domainNullifier  
`domain` - The domain of pages you want to domainNullifier  

```
$ python3 domainNullifier.py 1234-5678-9123-4567 www.domain.com  
```
Runs `domainNullifier.py` for pages on www.domain.com, nulling out the `domain` field for pages which have it set as the `domain` argument, allowing these pages to inherit the domain that is primary for their content type  for portal with access token `1234-5678-9123-4567`   

## cmsFinder.py
_REQUIRES_  
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  

_USAGE_  
This Python python figures out which CMS a page uses and grades it in PSI mobile and desktop. Requyires creating a Python list in `pagesToScrub` of the pages/sites to crawl, like: `pagesToScrub = ["http://www.puppy.com", "http://cats.com", ...]` 
```
$ python3 cmsFinder.py
```
This will output the CMS a site uses based on the `meta name="generator"` HTML tag. If there is no `generator` meta tag, we will look for some other common signs of certain CMSs.

## cdn1Replacer.py
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python finds cdn1 images in post bodies, creates a cdn2 version of the file, and updates the post body to use the new cdn2 image srcs. This Python python takes two agruments: `accessToken` & `contentGroupId`  
`accessToken` - An access_token for the portal you want to urlMappingSlothRestore  
`contentGroupId` - The blog object Id you wish to cdn1Replacer.py  
```
$ python3 cdn1Replacer.py 1234-5678-9123-4567  6053289841
```
This will look at the post bodies of all blog posts in blog id 6053289841, fnding all cdn1 image sources, creating a new cdn2 file, forumlating a new post body with the cdn2 image sources, and updating the blog post

## hubDangerZoneLasso.py
THIS IS SKETCHY, ONLY USE IN DIRE SITUATIONS 
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python finds ALL instances of a string, and replaces it with another STRING ANYWHERE in a page object. The string can be nested anywhere on the JSON tree of the page object and it will be replaced. The replaced page object is then PUT back and made live. This Python python takes four agruments: `accessToken`, `stringToLasso`, `lassoReplace` & `mode`  
`accessToken` - An access_token for the portal you want to urlMappingSlothRestore  
`stringToLasso` - The string to find  
`lassoReplace` - The string to replace with  
`mode` - Will not actually update anything unless this argument is equal to `write`
```
$ python3 hubDangerZoneLasso.py 1234-5678-9123-4567 findme replacewithme write
```
This will look at all page objects in portal with `access_token` 1234-5678-9123-4567, finding and replacing ALL INSTANCES OF "findme" with "replacewithme", and updating the page with the newwly replaced content