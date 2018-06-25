# contentDruid
A collection of Python scripts for various content object jobs. These are very powerful scripts, so please read the spec and use them with respect and ease. A _sloth_ is is a passive script, finding things for you.  
p.s. I like to call [Python](https://www.python.org/) scripts, "snakes." Why? Because it is fun :)

__filesSlothRestore__ - Find and restore deleted file objects  
## filesSlothRestore
A Python snake to find deleted file objects and restore them  
_REQUIRES_  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This snake takes three agruments: `accessToken`, `slothStart` and `slothEnd`  
`accessToken` - an accessToken for the portal you want to filesSlothRestore  
`slothStart` - A millisecond unix timestamp used in the `deleted_at__gt` request parameter to dictate the start time of file deletion timestamps to GET  
`slothEnd` - A millisecond unix timestamp used in the `deleted_at__lt` request parameter to dictate the end time of file deletion timestamps to GET  

```
$ filesSlothRestore.py 1234-5678-9123-4567 1529816400000 1529902800000
```
Runs `filesSlothRestore.py` finding files deleted between 1529816400000 (June 24th, 2018 0:00:00) and 1529902800000 (June 25th, 2018 0:00:00) for portal with access token `1234-5678-9123-4567`