# YARL-YetAnotherRancherLibrary
Yet another attempt to make a rancher compatible library for python 3, which supports 2-beta.

## This lib presents two classes:
### RancherCow - which is a main class for interferring with rancher. I'm updating it once I need new methods. 
### RancherAuthToken - This class contains methods to control(spawn/delete/disable) API keys for an environment if you wish so, using your admin credentials.

Usage: 
```
from RancherCow import RancherCow
from RancherAuthToken import RancherAuthToken


# initialize class
rauth = RancherAuthToken("htttp(s)//blah.com:8080", "login", "pass")
# unpack sc,ac,key_id
_secret_key, _acccess_key, _key_id = rauth.generate_api_token(name="foo", description="bar")


# initialize class
rancher = RancherCow('http(s)://blah.com:8080', "_acccess_key", "_secret_key", "rancher_env")
rancher.get_status_of_container(i1ad)

# remove key_id if neccessary
rauth.deactivate_api_token(_key_id)
rauth.delete_api_token(_key_id)
```
