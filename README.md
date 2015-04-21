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

**`list_google_users`** - *lists all google user accounts*

**`google_user`** - *returns user data for specific google account*

**`list_slack_users`** - *lists all slack user accounts*

**`slack_user`** - *returns user data for specific slack account*

**`list_hipchat_users`** - *lists all hipchat user acccounts*

**`hipchat_user`** - *returns user data for specific hipchat account*

**`list_user_services`** - *returns current user membership of all services*
