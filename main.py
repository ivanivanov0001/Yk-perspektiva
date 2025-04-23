
from aiogram import Bot, Dispatcher, executor, types
import os

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Здравствуйте! Я ваш помощник. Помогу вам быстро и удобно отправить заявку или сообщить о неисправности в вашу управляющую компанию.

Чтобы начать, пожалуйста, представьтесь. Мне понадобятся:
– ФИО
– Адрес (улица, дом, квартира)
– Номер телефона")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
