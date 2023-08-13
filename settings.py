#imports
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()
DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
STATUS: Optional[str] = os.getenv("STATUS")
TIMERS_FILE_PATH: Optional[str] = os.getenv("TIMERS_FILE_PATH")



def check_n_Handle_Key():
    global DISCORD_TOKEN
    if DISCORD_TOKEN is None:
        print('No value for DISCORD_TOKEN found')
        try:
            env_file = open('.env', 'x')
            print('No env file found. Creating file')
        except:
            env_file = open('.env')
            print(f'.env file already exists with data "{env_file.read()}".\nOpening file in append mode.')
            env_file.close()
            env_file = open('.env', 'a')
            print('File Opened')
        input_token = ''
        while input_token == '':
            input_token = input("Please enter your bot's token: ")
            if input_token == '':
                print('Invalid Discord Token')
        env_file.write(f'\nDISCORD_TOKEN={input_token}')
        env_file.close()
        print("Attempting to load new token")
        load_dotenv()
        DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        if DISCORD_TOKEN is None:
            raise ValueError(
                f'DISCORD_TOKEN Still has no value. There could be a permission issue with this script creating files. Please create the .env file manually and add the token by appending "DISCORD_TOKEN={input_token}" without the quotes.')
        print(f'DISCORD_TOKEN returned value of "{DISCORD_TOKEN}"')
        print('File Write successful')

def check_status():
    global STATUS
    if STATUS is None:
        print('No value for STATUS found')
        try:
            env_file = open('.env', 'x')
            print('No env file found. Creating file')
        except:
            env_file = open('.env')
            print(f'.env file already exists with data "{env_file.read()}".\nOpening file in append mode.')
            env_file.close()
            env_file = open('.env', 'a')
            print('File Opened')
        input_status = input("Please enter your bot's status (nothing to include give no status): ")
        env_file.write(f'\nSTATUS={input_status}')
        env_file.close()
        print("Attempting to load new token")
        load_dotenv()
        STATUS = os.getenv("STATUS")
        if STATUS is None:
            raise ValueError(
                f'STATUS Still has no value. There could be a permission issue with this script creating files. Please create the .env file manually and add the token by appending "STATUS={input_status}" without the quotes.')
        print(f'STATUS returned value of "{STATUS}"')
        print('File Write successful')


def check_settings():
    check_n_Handle_Key()
    check_status()
