from __future__ import annotations
from typing import Tuple
import re

class Time:
    def __init__(self, hours = 0, minutes = 0, seconds = 0, milliseconds = 0):
        ms, msr = self.calc(int(milliseconds), 1000)
        self.milliseconds = ms
        s, sr = self.calc(int(seconds) + msr, 60)
        self.seconds = s
        m, mr = self.calc(int(minutes) + sr, 60)
        self.minutes = m
        self.hours = int(hours) + mr
        assert abs(self.minutes) < 60, f'minutes: maximum value 60, actual {self.minutes}'
        assert abs(self.seconds) < 60, f'seconds: maximum value 60, actual {self.seconds}'
        assert abs(self.milliseconds) < 1000, f'milliseconds: maximum value 1000, actual {self.milliseconds}'

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

    def calc(self, value : int, maxval : int) -> Tuple[int, int]:
        realval = value % maxval
        return (realval, value // maxval)

    def __str__(self):
        return f'{self.hours:02}:{self.minutes:02}:{self.seconds:02},{self.milliseconds:03}'

    @classmethod
    def fromstr(cls, timestr : str) -> Time:
        hour, minute, second, millisecond = re.split(':|,', timestr)
        return cls(hour, minute, second, millisecond)


