# unaccountable

#### Under construction, this readme is purely for development purposes, check back later!

http://saxophonehorse.ytmnd.com/

##### Setup

OAuth nonsense TBC

Copy the sample config file below, and place it in the root folder, or run `python unaccountable.py` and type `configure`

*config.yml*
```
google_private_key_path: "/path/to/private/keyfile.p12"
service_account_email: "SOMETHING@dGOOGLE-DEVELOPER-ACCOUNT"
service_user_email: "USER@GOOGLEDOMAIN"
domain: "DOMAIN"
hipchat_auth_token: "AUTHTOKEN"
slack_auth_token: "AUTHTOKEN"
g_user_pw: "DEFAULT-GOOGLE-PASSWORD"
h_user_pw: "DEFAULT-HIPCHAT-PASSWORD"
```

##### Use

###### Available Commands

**`configure`** - *creates a config file from scratch or overwrites an existing one*

**`get_users [SERVICE]`** - *lists all users in a service*

**`get_user [SERVICE]`** - *returns user data from specified service*

**`get_user [USER_EMAIL]`** - *queries all services for that user account, returns a table of results
                               (booleans only)*

**`user_manifest [USER_EMAIL]`** - *returns all user data from all services which contain a record of
                                    that email address*

**`is_admin [USER_EMAIL]`** - *Returns a table of services (booleans only) specifying admin priveliges for
                               that account*
