from __future__ import annotations
import re

class Time:
    def __init__(self, hours = 0, minutes = 0, seconds = 0, milliseconds = 0):
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.seconds = int(seconds)
        self.milliseconds = int(milliseconds)

    def add(self, time : Time) -> Time:
        return self

    def __str__(self):
        return f'{self.hours:02}:{self.minutes:02}:{self.seconds:02},{self.milliseconds:03}'

    @classmethod
    def fromstr(cls, timestr : str) -> Time:
        hour, minute, second, millisecond = re.split(':|,', timestr)
        return cls(hour, minute, second, millisecond)


