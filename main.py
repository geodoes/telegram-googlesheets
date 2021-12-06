from pprint import pprint

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import logging
from aiogram import Bot, Dispatcher, executor, types



# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1teusj0gRLbg53ZdRDNDe0DT3IaCC_zY-1LQZA7j8jV0'
# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

"""БОТ"""
API_TOKEN = '5096148704:AAEZz7CtyneILL6I3lPCdROmQmLk1A68v3c'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Пример чтения файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A:D',
    majorDimension='ROWS'
).execute()

'''Здесь код вывода в телеграмм'''
@dp.message_handler(commands=['start'])
async def information(message: types.Message):
    await message.answer(
        "Для просмотра списков объектов введите: '/show'.\n\n"
        "Для просмотра реестра платежей: '/PaymentsShow'.\n\n"
        "Для добавления нового объекта введите '/add' и укажите информацию в следующем формате:\n\n"
        "Местоположения объекта| Отдел| Полное наименование КА| Внутреннее наименование\n\n"
        "Например внесем новый объект (все пишем в одну строчку(соблюдая пробелы и тире)):\n\n"
        "/add челябинск т ооо-ромашка парк-гагарина\n\n"
        "Для добавления нового платежа в реестр введите '/addPay' и укажите информацию в следующем формате:\n\n"
        "Срок Оплаты| Сумма прихода| Сумма Расхода| Дата поступения задачи| Кто поставил задачу| Кто оплатил| Проект| Суть расхода| Лицо принимающее платеж| Лицо кому предназначаются средства| Реквизиты для оплаты\n\n"
        "Например внесем новый запрос на платеж (все пишем в одну строчку(соблюдая пробелы и тире)):\n\n"
        "/addPay 5.дек нет 45000 3.дек Андрей Наталья ООО-Ромашка ЗП-Геодезисту Имангулов-Р-А Мамушкин-А-А 46164567876543\n\n"

    )


@dp.message_handler(commands=['show'])
async def show_objects_names(message: types.Message):
    nn = 0
    for i in range(0, len(values['values'])):
        await message.answer(values['values'][nn+1])
        nn +=1

@dp.message_handler(commands=["add"])
async def adding(message: types.Message):
    filtered = message.text.split()
    rows = [
        [filtered[1].upper(), filtered[2].upper(), filtered[3].upper(),filtered[4].upper(),message.from_user.username],
    ]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A:D",
        body={
            "majorDimension": "ROWS",
            "values": rows
        },
        valueInputOption="USER_ENTERED"
    ).execute()

@dp.message_handler(commands=['PaymentsShow'])
async def show_payments(message: types.Message):
    spreadsheet_id = '1AM1KfRs65f7pD_UPjO1jDFwYVy0Gw2zHd-mJJdrbsGY'
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A:Z',
        majorDimension='ROWS'
    ).execute()
    nn = 0
    for i in values['values'][int(len(values['values']))-50:]:
        await message.answer(i)


@dp.message_handler(commands=["addPay"])
async def adding_pay(message: types.Message):
    spreadsheet_id = '1AM1KfRs65f7pD_UPjO1jDFwYVy0Gw2zHd-mJJdrbsGY'
    filtered_pay = message.text.split()
    print(filtered_pay)
    rows_2 = [
        [filtered_pay[1].upper(), filtered_pay[2].upper(), filtered_pay[3].upper(),filtered_pay[4].upper(),filtered_pay[5].upper(),filtered_pay[6].upper(),filtered_pay[7].upper(),filtered_pay[8].upper(),filtered_pay[9],filtered_pay[10],filtered_pay[11],message.from_user.username],
    ]

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A:I",
        body={
            "majorDimension": "ROWS",
            "values": rows_2
        },
        valueInputOption="USER_ENTERED"
    ).execute()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


