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

    for service in valid_services:
        if service == "google":
            print "GOOGLE"
            res = gc.get_user_info(u_email)
            print "Is Delegated Admin: " + str(res["isDelegatedAdmin"])
            print "Is Admin: " + str(res["isAdmin"])
            print "======"
        elif service == "slack":
            print "SLACK"
            print sc.get_user_info(u_email)["is_admin"]
            print "======"
        elif service == "hipchat":
            print "HIPCHAT"
            print hc.get_user_info(u_email)["is_group_admin"]
            print "======"
