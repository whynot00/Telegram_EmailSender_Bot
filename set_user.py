import json




def wl_checker(user_id, powers):
    with open("configurations/white_list.json", "r") as file:
        white_list = json.load(file)

    for key in white_list[powers].keys():
        print("x")
        if user_id in white_list[powers][key]:
            return True

def all_members():


    with open("configurations/white_list.json", "r") as file:
        members = json.load(file)

        for key in members.keys():
            


all_members()
