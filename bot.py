# Imports
import discord
import settings
from discord import app_commands
from timeruser import TimerUser
from timer import UserTimer
from action import Action
import time

bot_users: [TimerUser] = []


def run_discord_bot():
    settings.check_settings()
    client = discord.Client(command_prefix="/", intents=discord.Intents.all())
    tree = app_commands.CommandTree(client)

    @tree.command(name='list', description='Lists timers or stopwatches linked to you')
    @app_commands.describe(option='Choose to lists specifically timers or stop watches')
    @app_commands.choices(
        option=[app_commands.Choice(name='Timers', value='1'), app_commands.Choice(name='Stop Watches', value='2')])
    async def list(interaction: discord.Interaction, option: app_commands.Choice[str]):
        await interaction.response.send_message('Checking for account in data base...', ephemeral=True)
        message = await interaction.original_response()
        if option.value == '1':
            return_message = 'There are no timers linked to your account.'
            for bot_user in bot_users:
                if bot_user.user_object.id == interaction.user.id:
                    await message.edit(content='Account found in database. Reading timers...')
                    return_message = 'Timers linked to your account\n'
                    for existing_timer in bot_user.timers:
                        return_message += (f'Name: {existing_timer.name}\nTimer length: {existing_timer.life_time} seconds\nTime left: ')
                        if existing_timer.end_time < time.time():
                            return_message += ('0 seconds\n')
                        else:
                            return_message += (f'{round(existing_timer.end_time - time.time())} seconds\n')
                        return_message += ('--------------------\n')
        await message.edit(content=return_message)


    @tree.command(name='create_test_timer', description='Creates a 1 minute timer for testing which notifies the user.')
    async def create_test_timer(interaction: discord.Interaction):
        await interaction.response.send_message('Creating timer...', ephemeral=True)
        message = await interaction.original_response()
        global bot_users
        user_exists = False
        to_many_timers = False
        if len(bot_users) != 0:
            for bot_user in bot_users:
                if bot_user.user_object.id == interaction.user.id:
                    user_exists = True
                    name_number = 1
                    recheck = True
                    while recheck:
                        recheck = False
                        for set_timer in bot_user.timers:
                            if set_timer.name == f'Test Timer {name_number}':
                                recheck = True
                                name_number += 1
                                break
                        if name_number > 40:
                            to_many_timers = True
                            break
                    bot_user.timers.append(UserTimer(starting_time=round(time.time()), life_time=60, name=f'Test Timer {name_number}',
                                                       set_action=Action.none, user=interaction.user,
                                                       set_channel=interaction.channel))
        if not user_exists:
            bot_users.append(TimerUser(user_object=interaction.user,
                                       timer=UserTimer(starting_time=round(time.time()), life_time=60, name='Test Timer 1',
                                                       set_action=Action.none, user=interaction.user,
                                                       set_channel=interaction.channel)))
        if to_many_timers:
            await message.edit(content='Too many test timers. Delete one before creating another timer.')
            return
        await message.edit(content='1 Minute timer created')

    @tree.command(name='create', description='Create a timer or stopwatch')
    @app_commands.choices(option=[app_commands.Choice(name='Timer', value='0')])
    async def create(interaction: discord.Interaction, option: app_commands.Choice[str]):
        if option.value == '0':
            print(f'User "{interaction.user.name}" requested timer creation')
        await interaction.response.send_message(f'Command received with option {option.name} chosen')

    @client.event
    async def on_ready():
        print(f'Bot loaded with Discord Token {settings.DISCORD_TOKEN}')
        if settings.STATUS != '':
            print(f'Changing bot status to "Playing {settings.STATUS}"')
            await client.change_presence(activity=discord.Game(f'{settings.STATUS}'))
        await tree.sync()

    client.run(settings.DISCORD_TOKEN)
