import httplib2
import pprint

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

class Google():
    def __init__(self, config):
        self.service_account = config["service_account_email"]
        self.sub_user_email = config["service_user_email"]
        self.domain = config["domain"]
        self.user_pass = config["google_user_pass"]

        with open(config["google_private_key_path"], 'rb') as p_key:
            self.private_key = p_key.read()
            p_key.close()

        http = httplib2.Http()
        """
            Sub account is needed to fulfill these actions
            http://stackoverflow.com/questions/20704925/google-admin-sdk-directory-api-403-python 
        """
        credentials = SignedJwtAssertionCredentials(
                        self.service_account,
                        self.private_key,
                        scope=["https://www.googleapis.com/auth/admin.directory.group",
                               "https://www.googleapis.com/auth/admin.directory.user"],
                        sub=self.sub_user_email
                      )
        http = credentials.authorize(http)
        self.directory_api = build('admin', 'directory_v1', http= http)

    def all_users(self):
        r = self.directory_api.users().list(domain=self.domain, maxResults=500).execute()
        users = []
        for user in r["users"]:
            users.append(user["primaryEmail"])
        return users

    def get_user(self, user):
        r = self.directory_api.users().get(userKey=user)
        try:
            return r.execute()
        except:
            return False

    def is_user_admin(self, user):
        try:
            if (self.get_user(user)["isAdmin"] | self.get_user(user)["isDelegatedAdmin"]):
                return True
        except:
            return False

    def create_user(self, user):
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
        create_user = self.directory_api.users().insert(body=user_settings)

        print "Generating default aliases"
        desired_aliases = generate_aliases(user)
        print "Validating aliases"
        valid_aliases = [validate_email(email, all_user_emails()) for email in desired_aliases if validate_email(email, all_user_emails()) is not None]
        create_user.execute()

        # New accounts do not appear immediately
        print "User created, sleeping for 5 seconds..."
        time.sleep(5)
        print str(user) + "created"
        print "Adding aliases..."
        add_aliases(user.split()[0].lower() + "@" + self.domain, valid_aliases)
        print "Aliases created"
        print "Account creation finished, printing results"
        pprint.pprint(get_user_info(user.split()[0].lower() + "@" + self.domain))

    # Move everything below here out to somewhere
    def generate_user_template(self, user, pw=None):
        """
        generates user template json necesssary to create a new user account
        - user: string, user's first and last name separated by whitespace
        - domain_name: string, email domain, e.g 'greatemail.com'
        - pass: string, default password for email account
        """
        if pw is None:
            pw = self.user_pass

        json = {
                "primaryEmail": user.split()[0].lower() + "@" + self.domain,
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

    def validate_email(self, email, unavailable_emails):
        """
        checks to see if email is available
        - email: string, email you wish to be added
        - unavailable_emails: list, emails that are unavailable
        """
        if email not in unavailable_emails:
            return email

    def all_user_emails(self):
        """
        lists all user emails, including aliases
        """
        r = self.directory_api.users().list(domain=self.domain, maxResults=500).execute()
        emails = []
        for user in r["users"]:
            for key in user["emails"]:
                emails.append(key.values()[-1].lower())
        return set(emails)

    # API doesn't let you set aliases at creation so you need to add them later
    def generate_aliases(self, user):
        """
        generates default aliases for new users
        - user: string, user's first and last name separated by white space
        - domain_name: string, email domain, e.g 'greatemail.com'
        """
        domain_name = self.domain
        user = user.lower().split()
        aliases = [
                   user[0] + "." + user[1] + "@" + domain_name,
                   user[0] + user[1] + "@" + domain_name
                  ]
        return aliases

    def add_aliases(self, user, aliases):
        """
        add aliases to an existing user, not possible at account creation
        - user: string, user email
        - aliases: list, aliases to be added
        """
        for als in aliases:
            service.users().aliases().insert(userKey=user, body={"alias": als}).execute()
