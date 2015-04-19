import google_create as gc
import hipchat_create as hc
import jira_create as jc
import slack_create as sc

def is_user_in(u_email, services):
    res = dict.fromkeys(services)
    for service in set(services):
        if service == "google":
            if gc.get_user_info(u_email):
                res["google"] = True
            else:
                res["google"] = False
        if service == "hipchat":
            if hc.get_user_info(u_email):
                res["hipchat"] = True
            else:
                res["hipchat"] = False
        if service == "jira":
            print ""
        if service == "slack":
            print ""

    return res
