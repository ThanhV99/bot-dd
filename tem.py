import os
import json
import argparse
import asyncio
import requests
from telegram import Bot
import dotenv


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


async def generate_token() -> str:
    url = "https://sapi.fpt.vn/token/GenerateToken"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'HRISProject/1879 CFNetwork/1399 Darwin/22.1.0',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Basic dGh1eWhrMkBmcHQuY29tLnZuOjEyMzQ1Ng=='
    }
    response = requests.request("GET", url, headers=headers)

    return response.text


async def perform_checkin_checkout(token: str, checkin_type: int) -> None:
    url = "https://sapi.fpt.vn/hrapi/api/services/app/Checkin/Checkin"
    payload = json.dumps({
        "SmartPhoneDeviceIMEI": "EA91F139-CC6C-4D94-AAAA-BD08C24466A1",
        "CheckinType": checkin_type
    })

    headers = {
        'content-type': 'application/json',
        'pragma': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer{token}',
        'currentversioncode': '1879',
        'expires': '0',
        'currentversion': '2.7.1',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache, no-store, must-revalidate',
        'platform': 'ios',
        'accept-encoding': 'gzip, deflate, br',
        'app-authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjUyNzM1IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6IkxvbmdIRDE0QGZwdC5jb20iLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6IkZER1pIRkFUTkNXQ0JPWE5PUTJaQ0RTV1hERlhRM09NIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiRW1wbG95ZWUiLCJodHRwOi8vd3d3LmFzcG5ldGJvaWxlcnBsYXRlLmNvbS9pZGVudGl0eS9jbGFpbXMvdGVuYW50SWQiOiIxIiwiRW1wbG95ZWVJZENsYWltIjoiNTI2NzkiLCJzdWIiOiI1MjczNSIsImp0aSI6IjViZjkxYmIzLWM1NDMtNGVlYy04ZDYwLTNkNDc3NzU5YzBhMyIsImlhdCI6MTY5NjU4MDA0MSwibmJmIjoxNjk2NTgwMDQxLCJleHAiOjE3MDQzNTYwNDEsImlzcyI6IkhSSVMiLCJhdWQiOiJIUklTIn0.F1_xcIspAmE7laQkSZKRyX2quG2BK2221HJ9-jN2xdY',
        'user-agent': 'HRISProject/1879 CFNetwork/1399 Darwin/22.1.0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code


async def send_telegram_message(message: str):
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def main():
    parser = argparse.ArgumentParser(
        description="Check-in or Check-out")
    parser.add_argument("--checkin", action="store_true",
                        help="Perform check-in.")
    parser.add_argument("--checkout", action="store_true",
                        help="Perform check-out.")

    args = parser.parse_args()

    if args.checkin or args.checkout:
        token = await generate_token()
        checkin_type = 1 if args.checkin else 2
        status_code = await perform_checkin_checkout(token, checkin_type)

        action = "Check-in" if args.checkin else "Check-out"
        if status_code == 200:
            await send_telegram_message(f"{action} successful!")
        else:
            await send_telegram_message(
                f"{action} failed with status code: {status_code}")
    else:
        print("Please provide either --checkin or --checkout.")

asyncio.run(main())