from aiogram import executor
from misc import dispatcher
import handlers
import support_files


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)