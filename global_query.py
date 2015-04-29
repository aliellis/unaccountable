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
            "asana": Asana(config)
        }

    def is_user(self, u_email):
        res = dict.fromkeys(self.services)

        for k, v in self.services.iteritems():
            if v.get_user(u_email):
                res[k] = True
            else:
                res[k] = False
        return res

    def is_user_admin(self, u_email):
        admin_s = ["slack", "hipchat", "google"]
        res = dict.fromkeys(admin_s)
        for service in admin_s:
            if self.services[service].is_user_admin(u_email):
                res[service] = True
            else:
                res[service] = False
        return res


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
