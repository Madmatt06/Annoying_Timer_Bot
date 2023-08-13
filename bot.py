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
    async def test(interaction: discord.Interaction, option: app_commands.Choice[str]):
        await interaction.response.send_message('You have nothing linked to your account.', ephemeral=True)

    @tree.command(name='create_test_timer', description='Creates a 1 minute timer for testing which notifies the user.')
    async def create_test_timer(interaction: discord.Interaction):
        global bot_users
        user_exists = False
        if len(bot_users) != 0:
            for bot_user in bot_users:
                if bot_user.user_object.id == interaction.user.id:
                    user_exists = True
        if not user_exists:
            bot_users.append(TimerUser(user_object=interaction.user,
                                       timer=UserTimer(starting_time=round(time.time()), life_time=60, name='timer1',
                                                       set_action=Action.none, user=interaction.user,
                                                       set_channel=interaction.channel)))
        await interaction.response.send_message('1 Minute timer created', ephemeral=True)

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
