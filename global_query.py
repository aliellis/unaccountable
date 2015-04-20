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
            if sc.get_user_info(u_email):
                res["slack"] = True
            else:
                res["slack"] = False

    return res


def is_user_admin_in(u_email, services):
    all_services = is_user_in(u_email, services)
    valid_services = [service for service, value in all_services.iteritems() if value is True]
    res = dict.fromkeys(services)

    for service in valid_services:
        if service == "google":
            google_q = gc.get_user_info(u_email)
            # Google has 2 defined admin roles, might need to expand this function
            if google_q["isDelegatedAdmin"] or google_q["isAdmin"]:
                res["google"] = True
            else:
                res["google"] = False
        elif service == "slack":
            res["slack"] = sc.get_user_info(u_email)["is_admin"]
        elif service == "hipchat":
            res["hipchat"] = hc.get_user_info(u_email)["is_group_admin"]
    return res
