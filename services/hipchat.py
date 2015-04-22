import json
import urllib2
import urllib
import urlparse


""" NOTE: Due to rate limiting, and the way HipChat handles user info requests,
    it is currently impossible to fetch ALL user data within a reasonable amount
    of time, this is because the 'user?'' call only returns about 1/2 of the 
    actual user information, crucially, the user's email address 
"""


class Hipchat():
    def __init__(self, config):
        self.endpoint = "https://api.hipchat.com/v2/"
        self.auth_token = config["hipchat_auth_token"]
        self.user_pass = config["hipchat_user_pass"]

    # Can probably remove this when we port over to requests
    # Necessary to handle white space in get_user_info requests
    def url_fix(s, charset='utf-8'):
        """Grabbed from http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python"""
        if isinstance(s, unicode):
            s = s.encode(charset, 'ignore')
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')
        qs = urllib.quote_plus(qs, ':&=')
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

    def all_users(self):
        url = self.endpoint + "user?auth_token=" + self.auth_token
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        response = response["items"]
        return [user["name"] for user in response]

    def get_user(self, user):
        url = self.endpoint + "user/" + user + "?auth_token=" + self.auth_token
        request = urllib2.Request(url)
        try:
            urllib2.urlopen(request)
            return json.load(urllib2.urlopen(request))
        except:
            # TODO: handle these exceptions!
            return False

    def create_user(user_email, user_name, user_mention, pw=None):
        if pw is None:
            pw = USER_PW
        host = "api.hipchat.com"
        url = "https://{0}/v2/user".format(host)
        headers = {'Content-type': 'application/json'}
        headers['Authorization'] = "Bearer " + AUTH_TOKEN
        params = {"auth_token": AUTH_TOKEN}
        payload = {
            'email': user_email,
            'name': user_name,
            'mention_name': user_mention,
            'password': pw
        }
        requests.post(url, params=params, data=json.dumps(payload), headers=headers)

    def get_all_rooms():
        url = self.endpoint + "room?auth_token=" + self.auth_token + "&private-room=true"
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        response = response["items"]
        return [room["name"] for room in response]

    def get_room_members(group):
        url = self.endpoint + "room/" + group + "?auth_token=" + self.auth_token
        url = url_fix(url)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        return [user["name"] for user in response["participants"]]
