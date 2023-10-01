import asyncio
import pyodbc
from config import host, user, password, db_name, tokens
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

bot = Bot(token=tokens)
dp = Dispatcher()

def connect_to_database():
    return pyodbc.connect(
        SERVER = host,
        DATABASE = db_name,
        USERNAME = user,
        PASSWORD = password
        # host=host,
        # user=user,
        # password=password,
        # database=db_name
    )
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={host};DATABASE={db_name};UID={user};PWD={password}'
conn = pyodbc.connect(connectionString) 
# Функция для поиска ответа в базе данных
def find_answer(question):
    conn = connect_to_database()
    cur = conn.cursor()

    query = ("SELECT answer FROM questions WHERE question = ?")
    parameter = question
    cur.execute(query, (parameter,))  # Используйте кортеж для параметров
    result = cur.fetchone()
    conn.close()

    return result

@dp.message()
async def cmd_question(message: Message):
    answer = find_answer(message.text)
    if answer:
        await message.reply(text=answer[0])
    else:
        await message.reply("Извините, я не могу найти ответ на ваш вопрос.")

@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer('''Привет, я отвечу на любые твои вопросы!
            Задавай же!''')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')