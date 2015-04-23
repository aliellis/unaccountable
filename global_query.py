from services.hipchat import Hipchat
from services.slack import Slack
from services.google import Google
from services.asana import Asana

class MultiQuery():
    def __init__(self, config):
        self.services = {
            "hipchat": Hipchat(config),
            "slack": Slack(config),
            "google": Google(config),
            # TODO: need get_user fun for asana
            # "asana": Asana(config)
        }

    def is_user(self, u_email):
        res = dict.fromkeys(self.services)

        for k, v in self.services.iteritems():
            if v.get_user(u_email):
                res[k] = True
            else:
                res[k] = False
        return res

# def services_user_is_in(u_email, all_services):
#     all_services = is_user_in(u_email, all_services)
#     return [service for service, value in all_services.iteritems() if value is True]
# 
# 
# def is_user_admin_in(u_email, services):
#     all_services = is_user_in(u_email, services)
#     valid_services = [service for service, value in all_services.iteritems() if value is True]
#     res = dict.fromkeys(services)
# 
#     for service in valid_services:
#         if service == "google":
#             google_q = gc.get_user_info(u_email)
#             # Google has 2 defined admin roles, might need to expand this function
#             if google_q["isDelegatedAdmin"] or google_q["isAdmin"]:
#                 res["google"] = True
#             else:
#                 res["google"] = False
#         elif service == "slack":
#             res["slack"] = sc.get_user_info(u_email)["is_admin"]
#         elif service == "hipchat":
#             res["hipchat"] = hc.get_user_info(u_email)["is_group_admin"]
#     return res
# 
# 
# def all_priveliges(u_email, all_services):
#     v_services = services_user_is_in(u_email, all_services)
#     res = dict.fromkeys(v_services)
# 
#     for service in v_services:
#         if service == "google":
#             res["google"] = gc.get_user_info(u_email)
#         elif service == "slack":
#             res["slack"] = sc.get_user_info(u_email)
#         elif service == "hipchat":
#             res["hipchat"] = hc.get_user_info(u_email)
#     return res
