from aiogram import executor
from misc import dispatcher
import handlers
import support_files

from support_files.parce_update_members_groups import client


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
    client.start()