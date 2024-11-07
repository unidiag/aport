#!/usr/bin/python3

import socket
import telegram  # pip install python-telegram-bot
import logging
import asyncio
import requests
import time


PORT = 22411        
TELEGRAM_TOKEN = '000000000:abcdefghijklmnopqrstuvwxyz'
CHAT_ID = '123456789' # id telegram
IPINFO_TOKEN = '11223344556677'  # token for api ipinfo.io
MESSAGE_INTERVAL = 60 # messages interval (1 min)



last_message_time = 0
bot = telegram.Bot(token=TELEGRAM_TOKEN)
logging.basicConfig(level=logging.INFO)


async def get_country_by_ip(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/country?token={IPINFO_TOKEN}')
        if response.status_code == 200:
            country = response.text.strip()
            return country
        else:
            logging.warning(f"Failed to get country for IP {ip_address}. Code: {response.status_code}")
            return "Unknown"
    except Exception as e:
        logging.error(f"Error getting country for IP {ip_address}: {e}")
        return "Unknown"


async def handle_connection(client_ip):

    global last_message_time
    current_time = time.time()

    if current_time - last_message_time >= MESSAGE_INTERVAL:
        try:
            country = await get_country_by_ip(client_ip)
            message = f"⚠️ Attempting connect to {PORT} from IP: {client_ip} ({country})"
            await bot.send_message(chat_id=CHAT_ID, text=message)
            logging.info(message)
            last_message_time = current_time
        except Exception as e:
            logging.error(f"Error sending message: {e}")
    else:
        logging.info(f"Message not sent. Interval less than {MESSAGE_INTERVAL} sec.")


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(1) # no more than 1 connection
    server_socket.setblocking(False)

    print(f"Server is running on port {PORT}...")

    while True:
        try:
            client_socket, client_address = await asyncio.get_event_loop().sock_accept(server_socket)
            client_ip = client_address[0]
            await handle_connection(client_ip)
            client_socket.close()
        except Exception as e:
            logging.error(f"ERROR: {e}")
            break

    server_socket.close()

asyncio.run(main())

