import asyncio
import schedule
import time
from aiogram import Bot, Dispatcher
import mysql.connector


USERS = ()
print(type(USERS))

def collecting_users_id():
    mydb.reconnect()
    mycursor = mydb.cursor()
    #проверка на наличие записи в БД
    mycursor.execute(f"SELECT user_id FROM `TARO_USERS` WHERE played_today=0")
    myresult = mycursor.fetchall()
    global USERS
    for i in myresult:
        temp_list = list(USERS)
        temp_list.append(i[0])
        USERS = tuple(temp_list)
    print(USERS)

collecting_users_id()



async def send_message(user_id, message):
    try:
        await bot.send_message(user_id, message)
        print(f"Сообщение успешно отправлено пользователю {user_id}")
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

async def send_messages():
    message = "🌠Время выбрать свою карту Таро!"
    tasks = [send_message(user_id, message) for user_id in USERS]
    await asyncio.gather(*tasks)

def job():
    asyncio.run(send_messages())

if __name__ == "__main__":
    bot = Bot(token='')
    dp = Dispatcher()

    # Планируем выполнение задачи каждый день в 8 утра
    schedule.every().day.at("08:00").do(job)

    print("Запланировано отправка сообщений каждый день в 8 утра.")

    while True:
        schedule.run_pending()
        time.sleep(1)
