from aiogram import Bot, Dispatcher, executor, types
import os
import json

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Простая база пользователей в виде словаря
users = {}

# Загружаем пользователей из файла, если он есть
if os.path.exists("users.json"):
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id in users:
        await message.answer("С возвращением! Выберите, что хотите сделать:\n\n— Отправить заявку\n— Сообщить о неисправности\n— Мои заявки")
    else:
        await message.answer("Здравствуйте! Я ваш помощник. Помогу вам быстро и удобно отправить заявку или сообщить о неисправности в вашу управляющую компанию.\n\nЧтобы начать, пожалуйста, представьтесь. Напишите ваше ФИО.")
        users[user_id] = {"step": "get_name"}
        save_users()

@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in users:
        await message.answer("Введите команду /start.")
        return

    user = users[user_id]

    if user.get("step") == "get_name":
        user["name"] = message.text
        user["step"] = "get_address"
        await message.answer("Спасибо! Теперь укажите адрес (улица, дом, квартира).")
    elif user.get("step") == "get_address":
        user["address"] = message.text
        user["step"] = "get_phone"
        await message.answer("Отлично! Теперь введите номер телефона.")
    elif user.get("step") == "get_phone":
        user["phone"] = message.text
        user["step"] = "done"
        await message.answer("Регистрация завершена! Теперь вы можете:\n\n— Отправить заявку\n— Сообщить о неисправности\n— Мои заявки")
    else:
        await message.answer("Пожалуйста, выберите действие из меню или введите /start.")

    save_users()

def save_users():
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
