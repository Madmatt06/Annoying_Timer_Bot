from action import Action
from discord import User, channel
import asyncio
from time import sleep


async def timer_send(user: User, set_channel: channel, timer_name: str, wait: int):
    print('timer_send function called')
    try:
        await asyncio.sleep(wait)
        await set_channel.send(f'{user.mention}\n The timer "{timer_name}" has gone off!')
    except asyncio.CancelledError:
        print('Timer cancled')
        return


async def timer_message(user: User, set_channel: channel, timer_name: str, wait: int, message_send: str):
    print('timer_message function called')
    try:
        await asyncio.sleep(wait)
        await set_channel.send(f'"{message_send}" \nTimer created by {user.mention}.')
    except asyncio.CancelledError:
        print('Timer cancled')
        return

class UserTimer:

    def __init__(self, starting_time: int, life_time: int, name: str, set_action: Action, user: User, set_channel: channel, action_arg: str = ''):
        self.starting_time = starting_time
        self.life_time = life_time
        self.end_time = starting_time + life_time
        self.name = name
        self.set_action = set_action
        self.user = user
        self.action_arg = action_arg
        self.Channel = set_channel
        self.async_timer_switch = {
            Action.none: timer_send(user=user, set_channel=set_channel, timer_name=name, wait=life_time),
            Action.ping: timer_send(user=user, set_channel=set_channel, timer_name=name, wait=life_time),
            Action.message: timer_message(user=user, set_channel=set_channel, timer_name=name, wait=life_time, message_send=action_arg)
        }

        self.async_timer = asyncio.create_task(self.async_timer_switch.get(set_action))

    def __del__(self):
        self.async_timer.cancel()