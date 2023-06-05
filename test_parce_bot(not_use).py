from telethon.sync import TelegramClient, events
from telethon import connection
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsRecent
from telethon.tl.functions.channels import GetParticipantsRequest

import sqlite3

from configurations import configuration_file as config

api_id = config.configuration_data["TELETHON_API_ID"]
api_hash = config.configuration_data["TELETHON_API_HASH"]
username = config.configuration_data["TELETHON_USERNAME"]
# group_href = ['https://t.me/drop_farsen', 'https://t.me/saledroppp']

client = TelegramClient(username, api_id, api_hash)


members_str_username = []


async def main(client):
    with open("configurations/groups_members.txt") as file:
        group_href = file.read().split(", ")
    print(group_href)
    # group_href = ['https://t.me/drop_farsen', 'https://t.me/saledroppp']
    con = sqlite3.connect("logs/member_list.db")
    cur = con.cursor()

    # for item_group in group_href:
    #     namegroup = item_group.replace('https://t.me/', '')
    #     cur.execute(f"CREATE TABLE IF NOT EXISTS {namegroup}(username TEXT,userid TEXT);")
        
    #     chat_entity = await client.get_entity(item_group)
    #     offset = 0

    #     print(f"Сейчас: {namegroup}")
    #     while True:
    #         participants =  await client(GetParticipantsRequest(chat_entity, filter=ChannelParticipantsSearch(q=""), offset=offset, limit=200, hash=200))
    #         if not participants.users:
    #             break
            
    #         for user in participants.users:
    #             members_str_username.extend((user.username, user.id))
    #             cur.execute(f"INSERT INTO {namegroup} VALUES(?, ?);", members_str_username)
    #             members_str_username.clear()
    #         offset += int(len(participants.users))
    #         print(offset)
        
    # con.commit()
        



if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main(client))



