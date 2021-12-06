from pprint import pprint

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import logging
from aiogram import Bot, Dispatcher, executor, types




CREDENTIALS_FILE = 'YOUR CREDENTIALS FROM GOOGLE DEVELOPERS CONSOLE'
spreadsheet_id = 'YOUR SPREADSHEETID FROM GOOGLE SHEETS(YOU CAN TAKE IT FROM URL)'
# AUTHORISATION
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

"""BOT ON"""
API_TOKEN = 'YOUR TELEGRAM BOT TOKEN'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# READ GOOGLESHEET
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A:D',
    majorDimension='ROWS'
).execute()

#CODE
@dp.message_handler(commands=['start'])
async def information(message: types.Message):
    await message.answer(
        "TO GET OBJECT LIST FROM FILE-1: '/show'.\n\n"
        "TO GET PAYMENT PLANNING LIST IN FILE-2: '/PaymentsShow'.\n\n"
        "TO ADD NEW OBJECT IN FILE-1:'/add' AND FOLOW THE EXAMPLE FURTHER:\n\n"
        "OBJECT LOCATION| CREW| FULL NAME OF COSTUMER| ONBOARD NAME OF COSTUMER\n\n"
        "EXAMPLE (ATTENTION ON SPACES(USE '-' INSTEAD SPACING)):\n\n"
        "/add MONTENEGRO SURVEYORS GIS-SAINS TIVAT-AEROPORT\n\n"
        "TO INSERT A NEW PAYMENT TO PLAN IN FILE-2  '/addPay' AND FOLOW THE EXAMPLE FURTHER:\n\n"
        "DATE TO PAY| MONEY CAME AMOUNT| MONEY SPENT| DATE OF TASK ADDED| WHO ADDED| WHOE MADE A TRANSACTION| PROJECT NAME| PAYMENT PURPOSE| WHO RECEVING MONEY| TO WHO MONEY ARE BELONG| CARD NUMBER\n\n"
        "EXAMPLE (ATTENTION ON SPACES(USE '-' INSTEAD SPACING)):\n\n"
        "/addPay 5.DEC NONE 4000 3.DEC MARK NATALY GIS-SAINS SURVEYOR-SALARY JONH-SMITH-JR NEO-FROM-MATRIX 2345 3333 3333 4444\n\n"

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
    spreadsheet_id = 'YOUR SPREAD SHEET - 2 USE IT IF U WORK IN DIFFERENT FILES'
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
    spreadsheet_id = 'YOUR SPREAD SHEET - 2 USE IT IF U WORK IN DIFFERENT FILES'
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


