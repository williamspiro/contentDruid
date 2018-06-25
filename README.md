# contentDruid
A collection of Python scripts for various content object jobs. These are very powerful scripts, so please read the spec and use them with respect and ease. A _sloth_ is is a passive script, finding things for you.  
p.s. I like to call [Python](https://www.python.org/) scripts, "snakes." Why? Because it is fun :)

__filesSlothRestore__ - Find and restore deleted file objects 
__blogFeaturedImageSoup__ - Soup featured images from an external blog, upload them to the File Manager, set them as featured for the posts respective HubSpot equivalent
## filesSlothRestore
A Python snake to find deleted file objects and restore them  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This snake takes three agruments: `accessToken`, `slothStart` & `slothEnd`  
`accessToken` - an accessToken for the portal you want to filesSlothRestore  
`slothStart` - A millisecond unix timestamp used in the `deleted_at__gt` request parameter to dictate the start time of file deletion timestamps to GET  
`slothEnd` - A millisecond unix timestamp used in the `deleted_at__lt` request parameter to dictate the end time of file deletion timestamps to GET  

```
$ filesSlothRestore.py 1234-5678-9123-4567 1529816400000 1529902800000
```
Runs `filesSlothRestore.py` finding files deleted between 1529816400000 (June 24th, 2018 0:00:00) and 1529902800000 (June 25th, 2018 0:00:00) for portal with access token `1234-5678-9123-4567`  

## blogFeaturedImageSoup
A Python snake to find the featured image on an external blog, upload it to the HubSpot File Manager, and then set the HubSpot hosted version of the posts' `featuredImage` with the newly uploaded File Manager asset  
_REQUIRES_  
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This snake requires manually setting 4 variables: `accessToken`, `blogRootUrl`, `featuredImageSelector` & `postsToSoupScrubKitten`

`accessToken` - Access token generated for __portalId__ (ex. `1234-5678-9123-456-789`)  
`blogRootUrl`- The external blogs root url (ex. http://www.blogrooturl.com/)  
`featuredImageSelector` - The CSS selector which select the external blogs featured image (ex. `.featured-image img`)  
`postsToSoupScrubKitten` - A python list of the slugs of all of the external posts to soup (ex. `["slug/post/1", "slug/post/2", "slug/post/3"]`)  

It is important that the post slugs of the external and HubSpot posts are the same. `blogRootUrl` + `postsToSoupScrubKitten[slugs]` should equal the actual URL of the posts. `slug`s should not start with a `/`, rather, `blogRootUrl` should end with a `/`

```
$ python blogFeaturedImageSoupScrubKitten.py
```