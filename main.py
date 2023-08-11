# Imports
import discord
from discord.ext import commands
from settings import check_n_Handle_Key, DISCORD_TOKEN



# Entry point
if __name__ == '__main__':
    check_n_Handle_Key()
    print(f'Loading bot with Token "{DISCORD_TOKEN}"')
