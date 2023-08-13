from enum import Enum


class Action(Enum):
    none = 'None'
    message = 'Message'
    ping = 'Ping'
    ping_message = 'Ping and Message'
    set_self_nick = 'set your own nickname'
    set_nick = 'set nickname'
    command = 'Execute Command'
