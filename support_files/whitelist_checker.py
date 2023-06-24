from aiogram import types
import json


def whitelist_checker(user_id, powers):
    with open("configurations/white_list.json", "r") as file:
        white_list = json.load(file)

    for key in white_list[powers].keys():
        if str(user_id) in white_list[powers][key]:
            return True

def all_users():

    with open("configurations/white_list.json", "r") as file:
        members = json.load(file)

    admin = ""
    moderators = ""
    users = ""

    for key in members.keys():
        if key == "admin":
            for item in members[key]:
                if len(members[key][item]) == 2:
                    admin += f"{members[key][item][0]} ({members[key][item][1]})\n"
                else:
                    admin += f"{members[key][item][0]}\n"

        elif key == "moderator":
            for item in members[key]:
                if len(members[key][item]) == 2:
                    moderators += f"{members[key][item][0]} ({members[key][item][1]})\n"
                else:
                    moderators += f"{members[key][item][0]}\n"
        
        elif key == "users":
            for item in members[key]:
                if len(members[key][item]) == 2:
                    users += f"{members[key][item][0]} ({members[key][item][1]})\n"
                else:
                    users += f"{members[key][item][0]}\n"

    return admin, moderators, users

def check_username(user_id, username):
    with open("configurations/white_list.json", "r") as file:
        white_list = json.load(file)

    for power in white_list.keys():
        for key_0 in white_list[power].keys():
            if (user_id in white_list[power][key_0]) and (len(white_list[power][key_0]) < 2):
                white_list[power][key_0].append(username)

    with open("configurations/white_list.json", "w") as file:
        json.dump(white_list, file)


