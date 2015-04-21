import pprint
import json
import urllib2
import yaml
import time
from fn_cache import Memoized

import ipdb

import urllib
import urlparse

config = open("config.yml", "r")
config = yaml.load(config)

AUTH_TOKEN = config["hipchat_auth_token"]
USER_PW = config["h_user_pw"]
ENDPOINT = "https://api.hipchat.com/v2/"


def all_users():
    # TODO: create a function that you pass 'name', 'email', 'rights', etc 
    # to make this more modular
    url = ENDPOINT + "user?auth_token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    response = response["items"]
    return [user["name"] for user in response]


def all_rooms():
    url = ENDPOINT + "room?auth_token=" + AUTH_TOKEN + "&private-room=true"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    response = response["items"]
    return [room["name"] for room in response]


def get_user_info(user):
    url = ENDPOINT + "user/" + user + "?auth_token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    try:
        urllib2.urlopen(request)
        return json.load(urllib2.urlopen(request))
    except:
        # TODO: handle these exceptions!
        return False


def get_room_members(group):
    url = ENDPOINT + "room/" + group + "?auth_token=" + AUTH_TOKEN
    url = url_fix(url)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    return [user["name"] for user in response["participants"]]


def url_fix(s, charset='utf-8'):
    """Grabbed from http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python"""
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


def detect_duplicate():
    return

@Memoized
def all_user_info():
    # full json response for all users
    url = ENDPOINT + "user?auth_token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    return response["items"]


def generate_unique_identifiers():
    res = {
           "mention_name": [],
           "email": [],
           "name": []
          }

    print "Generating..."
    all_info = all_user_info()
    for user in all_info:
        # import ipdb
        # ipdb.set_trace()
        print "adding uniques from " + user["name"]
        res["email"].append(get_user_info(str(user["id"]))["email"])
        res["mention_name"].append(user["mention_name"])
        res["name"].append(user["name"])
        print "uniques added, sleeping for 20 seconds to avoid rate limiting"
        # time.sleep(20)
    return res

# @Memoized
# def fibonacci(n):
#     "Return the nth fibonacci number."
#     if n in (0, 1):
#         return n
#     return fibonacci(n-1) + fibonacci(n-2)
# 
# print fibonacci(12)


    # json = {
    #         "email": 'test',
    #         "name:" 'test',
    #         "mention_name": 'test',
    #         "password": 'test'
    #        }
    # return json


print generate_unique_identifiers()
