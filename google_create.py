def add_aliases(user, aliases):
    """
    add aliases to an existing user, not possible at account creation
    - user: string, user email
    - aliases: list, aliases to be added
    """
    for als in aliases:
        service.users().aliases().insert(userKey=user, body={"alias": als}).execute()


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
