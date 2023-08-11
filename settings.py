#imports
from dotenv import load_dotenv
import os
from typing import Optional

global DISCORD_TOKEN
load_dotenv()
DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")


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
            input_token = remove_Suf_Pre_Spaces(input_token)
            if input_token == '':
                print('Invalid Discord Token')
        env_file.write(f'DISCORD_TOKEN={input_token}')
        env_file.close()
        print("Attempting to load new token")
        load_dotenv()
        DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        if DISCORD_TOKEN is None:
            raise ValueError(
                f'DISCORD_TOKEN Still has no value. There could be a permission issue with this script creating files. Please create the .env file manually and add the token by appending "DISCORD_TOKEN={input_token}" without the quotes.')
        print(f'DISCORD_TOKEN returned value of "{DISCORD_TOKEN}"')
        print('File Write successful')
