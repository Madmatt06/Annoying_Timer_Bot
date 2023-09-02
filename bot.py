# Imports
import discord
import settings
from discord import app_commands
from timeruser import TimerUser
from timer import UserTimer
from action import Action
import time
import views

bot_users: [TimerUser] = []


def run_discord_bot():
    settings.check_settings()
    client = discord.Client(command_prefix="/", intents=discord.Intents.all())
    tree = app_commands.CommandTree(client)

    @tree.command(name='list', description='Lists timers or stopwatches linked to you')
    @app_commands.describe(option='Choose to lists specifically timers or stop watches')
    @app_commands.choices(option=[app_commands.Choice(name='Timers', value='1'), app_commands.Choice(name='Stop Watches', value='2')])
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
    @app_commands.choices(minutes=[app_commands.Choice(name='1', value=1), app_commands.Choice(name='2', value=2), app_commands.Choice(name='3', value=3), app_commands.Choice(name='4', value=4), app_commands.Choice(name='5', value=5), app_commands.Choice(name='6', value=6), app_commands.Choice(name='7', value=7), app_commands.Choice(name='8', value=8), app_commands.Choice(name='9', value=9), app_commands.Choice(name='10', value=10), app_commands.Choice(name='30', value=30), app_commands.Choice(name='60', value=60), app_commands.Choice(name='120', value=120), app_commands.Choice(name='180', value=180), app_commands.Choice(name='240', value=240), app_commands.Choice(name='300', value=300),app_commands.Choice(name='360', value=360),app_commands.Choice(name='420', value=420),app_commands.Choice(name='480', value=480), app_commands.Choice(name='540', value=540)])
    @app_commands.choices(alarm=[app_commands.Choice(name='Notify', value=0), app_commands.Choice(name='Message', value=1)])
    @app_commands.describe(messagecommand = "Enter the message to send when the timer expires")
    async def create_test_timer(interaction: discord.Interaction, minutes: app_commands.Choice[int], alarm: app_commands.Choice[int], messagecommand: str):
        print(f'Recived test timer command from {interaction.user.name} with minutes = {minutes.name}, alarm = {alarm.name} and value = {alarm.value}, and messagecommand = {messagecommand}')
        service_limit:int = -1
        if interaction.user.id == 0:
            print(f'User {interaction.user.name} has a service rate limit of 1 timer at a time.')
            service_limit = 1
        current_timer_number:int = 0
        if alarm == 0:
            setalarm = Action.ping
        else:
            setalarm = Action.message
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
                    current_timer_number = len(bot_user.timers)
                    if current_timer_number >= service_limit and service_limit > -1:
                        print(f'User ({interaction.user.name}) has reached their service limit ("Current use" = {current_timer_number})')
                        await message.edit(content=f'You have reached your service limit of 1 timer at a time. Please clear timers with the "/delete timers" command')
                        return
                    bot_user.timers.append(UserTimer(starting_time=round(time.time()), life_time=minutes.value*60, name=f'Test Timer {name_number}',
                                                     set_action=setalarm, user=interaction.user,
                                                     set_channel=interaction.channel, action_arg= messagecommand))
        if not user_exists:
            bot_users.append(TimerUser(user_object=interaction.user,
                                       timer=UserTimer(starting_time=round(time.time()), life_time=minutes.value*60, name='Test Timer 1',
                                                       set_action=setalarm, user=interaction.user,
                                                       set_channel=interaction.channel, action_arg=messagecommand)))
        if to_many_timers:
            await message.edit(content='Too many test timers. Delete one before creating another timer.')
            return

        await message.edit(content=f'{minutes.name} minute timer created')

    @tree.command(name='create', description='Create a timer or stopwatch')
    @app_commands.choices(option=[app_commands.Choice(name='Timer', value='0')])
    async def create(interaction: discord.Interaction, option: app_commands.Choice[str]):
        if option.value == '0':
            print(f'User "{interaction.user.name}" requested timer creation')
        await interaction.response.send_message(content=f'Command received with option {option.name} chosen', view= views.timer_creation())

    @tree.command(name='delete', description='Delete a timer or stopwatch')
    @app_commands.choices(option=[app_commands.Choice(name='Timers', value=0)])
    async def create(interaction: discord.Interaction, option: app_commands.Choice[int]):
        if len(bot_users) != 0:
            await interaction.response.send_message('Searching for user timers...', ephemeral=True)
            message = await interaction.original_response()
            for bot_user in bot_users:
                if bot_user.user_object.id == interaction.user.id:
                    bot_user.timers = []
                    await message.edit(content='Timers removed succesfully.')
                    return
            await message.edit(content='Could not find any timers.')
            return
        else:
            await interaction.response.send_message('Could not find any timers.', ephemeral=True)
            return



    @client.event
    async def on_ready():
        print(f'Bot loaded with Discord Token {settings.DISCORD_TOKEN}')
        if settings.STATUS != '':
            print(f'Changing bot status to "Playing {settings.STATUS}"')
            await client.change_presence(activity=discord.Game(f'{settings.STATUS}'))
        await tree.sync()

    client.run(settings.DISCORD_TOKEN)
