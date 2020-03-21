from __future__ import annotations
import re

class Time:
    def __init__(self, hours = 0, minutes = 0, seconds = 0, milliseconds = 0):
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.seconds = int(seconds)
        self.milliseconds = int(milliseconds)

    def add(self, time : Time) -> Time:
        mssum = self.milliseconds + time.milliseconds
        self.milliseconds = mssum % 1000
        msrest = 0
        if mssum >= 1000:
            msrest = 1

        ssum = self.seconds + time.seconds + msrest
        self.seconds = ssum % 60
        srest = 0
        if ssum >= 60:
           srest = 1

        msum = self.minutes + time.minutes + srest
        self.minutes = msum % 60
        mrest = 0
        if msum >= 60:
           mrest = 1

        self.hours = self.hours + time.hours + mrest

        return self

    def __str__(self):
        return f'{self.hours:02}:{self.minutes:02}:{self.seconds:02},{self.milliseconds:03}'

    @classmethod
    def fromstr(cls, timestr : str) -> Time:
        hour, minute, second, millisecond = re.split(':|,', timestr)
        return cls(hour, minute, second, millisecond)


