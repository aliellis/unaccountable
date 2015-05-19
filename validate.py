import re


def validate_user(user):
    return True if re.match(".*?@.*?\.com", user) else False


def validate_i_in_list(group, valid_groups):
    if group not in valid_groups:
        print("{} not in valid list: {}").format(
            item, valid_list)
        return False

    else:
        return True
