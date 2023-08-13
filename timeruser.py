from discord import User, channel
from timer import UserTimer


class TimerUser:
    def __init__(self, user_object: User, timer: UserTimer = None):
        self.user_object: User = user_object
        self.timers: [UserTimer] = []
        if timer is not None:
            self.timers.append(timer)
