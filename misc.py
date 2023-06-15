import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
import configurations as config


token = config.configuration_file.configuration_data["TOKEN"]
bot = Bot(token=token, parse_mode="HTML")
memorystorage = MemoryStorage()

dispatcher = Dispatcher(bot, storage=memorystorage)
logging.basicConfig(level=logging.INFO)