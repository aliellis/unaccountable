import time
import ipdb
import httplib2
import json
import yaml
import pprint
import urllib2

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import SignedJwtAssertionCredentials

with open("pk.pem", 'rb') as f:
    private_key = f.read()
    f.close()

config = open("config.yml", "r")
config = yaml.load(config)

SERVICE_ACCOUNT_EMAIL = config["service_account_email"]
SERVICE_USER_EMAIL = config["service_user_email"]
SERVICE_DOMAIN = config["domain"]
USER_PW = config["g_user_pw"]

http = httplib2.Http()
credentials = SignedJwtAssertionCredentials(
                                            SERVICE_ACCOUNT_EMAIL,
                                            private_key,
                                            scope=["https://www.googleapis.com/auth/admin.directory.group",
                                                   "https://www.googleapis.com/auth/admin.directory.user"],
                                            sub=SERVICE_USER_EMAIL
                                           )

http = credentials.authorize(http)

service = build('admin', 'directory_v1', http= http)


def all_groups():
    """
    list all email groups
    """
    r = service.groups().list(domain= SERVICE_DOMAIN).execute()
    groups = []
    for group in r["groups"]:
        groups.append(group["email"])
    return groups


def all_users():
    """
    list all user emails
    """
    r = service.users().list(domain= SERVICE_DOMAIN).execute()
    users = []
    for user in r["users"]:
        users.append(user["primaryEmail"])
    return users


def all_user_emails():
    """
    lists all user emails, including aliases
    """
    r = service.users().list(domain= SERVICE_DOMAIN).execute()
    emails = []
    for user in r["users"]:
        for key in user["emails"]:
            emails.append(key.values()[-1].lower())
    return set(emails)


def get_user_info(user):
    """
    - user: string, user email
    """
    r = service.users().get(userKey=user)
    try:
        return r.execute()
        # return service.user().get(userKey=use
    except:
        # TODO: handle 404 exceptions as that means there is not user
        return False


def get_group_members(group):
    """
    - group: string, group email
    """
    r = service.members().list(groupKey=group).execute()
    members = r["members"]
    member_list = [user["email"] for user in members]
    return member_list


def generate_user_template(user, pw=None):
    """
    generates user template json necesssary to create a new user account
    - user: string, user's first and last name separated by whitespace
    - domain_name: string, email domain, e.g 'greatemail.com'
    - pass: string, default password for email account
    """
    if pw is None:
        pw = USER_PW

    json = {
            "primaryEmail": user.split()[0].lower() + "@" + SERVICE_DOMAIN,
            "name": {
                     "givenName": user.split()[0],
                     "familyName": user.split()[1],
                     "fullName": user
                    },
            "password": pw,
            "changePasswordAtNextLogin": True,
            "agreedToTerms": False
            }
    return json


def add_aliases(user, aliases):
    """
    add aliases to an existing user, not possible at account creation
    - user: string, user email
    - aliases: list, aliases to be added
    """
    for als in aliases:
        service.users().aliases().insert(userKey=user, body={"alias": als}).execute()


def create_user(user):
    """
    creates a user account, along with firstnamelastname@[domain_name] and
    firstname.lastname@[domain_name] aliases (if available) and adds them to a
    default group
    - user: string, user to be created, first name and last name separated by
    whitespace
    - group: list, groups user to be added to
    - domain_name: string, email domain, e.g 'greatemail.com'
    """
    print "Generating user template"
    user_settings = generate_user_template(user)
    create_user = service.users().insert(body=user_settings)

    print "Generating default aliases"
    desired_aliases = generate_aliases(user)
    print "Validating aliases"
    valid_aliases = [validate_email(email, all_user_emails()) for email in desired_aliases if validate_email(email, all_user_emails()) is not None]
    create_user.execute()

    # New accounts do not appear immediately, sleeping gives time for it to
    # appear for the alias generation
    print "User created, sleeping for 5 seconds..."
    time.sleep(5)
    print str(user) + "created"
    print "Adding aliases..."
    add_aliases(user.split()[0].lower() + "@" + SERVICE_DOMAIN, valid_aliases)
    print "Aliases created"
    print "Account creation finished, printing results"
    pprint.pprint(get_user_info(user.split()[0].lower() + "@" + SERVICE_DOMAIN))


# API doesn't let you set aliases at creation so you need to add them later
def generate_aliases(user, domain_name=None):
    """
    generates default aliases for new users
    - user: string, user's first and last name separated by white space
    - domain_name: string, email domain, e.g 'greatemail.com'
    """
    if domain_name is None:
        domain_name = SERVICE_DOMAIN
    user = user.lower().split()
    aliases = [
               user[0] + "." + user[1] + "@" + domain_name,
               user[0] + user[1] + "@" + domain_name
              ]
    return aliases


def validate_email(email, unavailable_emails):
    """
    checks to see if email is available
    - email: string, email you wish to be added
    - unavailable_emails: list, emails that are unavailable
    """
    if email not in unavailable_emails:
        return email


def add_to_group(email, group):
    r = service.users().groups()
    return
