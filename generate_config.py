def generate_config():
    g_service_account_email = raw_input("Google Service Account Email: ")
    g_service_user_email = raw_input("Google Service User Email: ")
    g_domain = raw_input("Google Domain: ")
    h_auth = raw_input("Hipchat AuthToken: ")
    s_auth = raw_input("Slack AuthToken: ")
    keys = ["service_account_email: ", "service_user_email: ", "domain: ",
            "hipchat_auth_token: ", "slack_auth_token: "]
    values = [g_service_account_email, g_service_user_email, g_domain,
              h_auth, s_auth]
    config = dict(zip(keys, values))

    file = open("config.yml", "w+")
    for k, v in config.iteritems():
        line = str(k + v)
        file.writelines(line + "\n")
    file.close()
