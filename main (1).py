import telebot
from datetime import datetime
import requests

# Токен вашого бота
token = "7703082565:AAE1c7FEkQwBT0ie9qygqLLAOjVbo9ibhGE"
bot = telebot.TeleBot(token)

# Функція для отримання історичних подій
def get_historical_events():
    today = datetime.now()
    day = today.day
    month = today.month
    url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"

    try:
        response = requests.get(url)
        data = response.json()
        events = data.get("events", [])
        
        if not events:
            return "На жаль, на сьогодні немає історичних подій."

        message = f"Історичні події на {day}.{month}:\n\n"
        for event in events[:5]:  # Отримуємо максимум 5 подій
            year = event.get("year", "Невідомий рік")
            description = event.get("description", "Немає опису")
            message += f"• {year}: {description}\n"
        return message
    except Exception as e:
        return f"Сталася помилка під час отримання інформації: {e}"

# Обробник команд старту
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Вітаю! Я Історичний бот. Надішліть команду /today, щоб дізнатися про події, що відбулися сьогодні в історії."
    )

# Обробник команди "today"
@bot.message_handler(commands=["today"])
def send_today_events(message):
    events = get_historical_events()
    bot.reply_to(message, events)

# Основний цикл бота
if __name__ == "__main__":
    bot.infinity_polling()
