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


client = TelegramClient(username, api_id, api_hash)


members_str_username = []


async def main(client):
    with open("configurations/groups_members.txt") as file:     # Открываем файл со списком групп для парсинга
        group_href = file.read().split(", ")

    con = sqlite3.connect("logs/member_list.db")    # Открываем db файл для записи спарсеных данных
    cur = con.cursor()

    # Проходим циклом по ссылкам групп в открытом выше файле
    for item_group in group_href:  
        namegroup = item_group.replace('https://t.me/', '')
        cur.execute(f"CREATE TABLE IF NOT EXISTS {namegroup}(username TEXT,userid TEXT);")  # Создаем таблицу под каждую группу
        
        chat_entity = await client.get_entity(item_group)   # Получаем сущность для парсинга
        offset = 0

        # Цикл для парсинга, сделан по гайдам, смещение offset каждые 200 пользователей
        while True:
            participants =  await client(GetParticipantsRequest(chat_entity, filter=ChannelParticipantsSearch(q=""), offset=offset, limit=200, hash=200))
            if not participants.users:
                break
            
            # Костыльная, но рабочая запись спарсшеных данных
            for user in participants.users:
                members_str_username.extend((user.username, user.id))
                cur.execute(f"INSERT INTO {namegroup} VALUES(?, ?);", members_str_username)
                members_str_username.clear()
            offset += int(len(participants.users))
        
    con.commit()    # Закрываем SQL
        



if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main(client))



