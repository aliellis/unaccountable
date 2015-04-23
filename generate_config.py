def generate_config():
    g_pk_path = raw_input("Location of Google Service P12 file (full path): ")
    g_account_email = raw_input("Google Service Account Email: ")
    g_user_email = raw_input("Google Service User Email: ")
    g_domain = raw_input("Google Domain: ")
    h_auth = raw_input("Hipchat AuthToken: ")
    s_auth = raw_input("Slack AuthToken: ")
    g_userpw = raw_input("Default password for new Google accounts: ")
    h_userpw = raw_input("Default password for new HipChat accounts: ")

    keys = ["google_private_key_path", "service_account_email: ",
            "service_user_email: ", "domain: ", "hipchat_auth_token: ",
            "slack_auth_token: ", "g_user_pw", "h_user_pw"]
    values = [g_service_account_email, g_service_user_email, g_domain,
              h_auth, s_auth]
    config = dict(zip(keys, values))

    file = open("config.yml", "w+")
    for k, v in config.iteritems():
        line = str(k + v)
        file.writelines(line + "\n")
    file.close()
