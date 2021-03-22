from __future__ import annotations
from typing import Tuple
import re

class Time:
    def __init__(self, hours = 0, minutes = 0, seconds = 0, milliseconds = 0):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0
        self.__add_with_values(int(hours), int(minutes), int(seconds), int(milliseconds))

    def __add__(self, time : Time) -> Time:
        return self.add(time)

    def add(self, time : Time) -> Time:
        self.__add_with_values(time.hours, time.minutes, time.seconds, time.milliseconds)
        return self

    def __str__(self):
        return f'{self.hours:02}:{self.minutes:02}:{self.seconds:02},{self.milliseconds:03}'

    def __add_with_values(self, hours: int, minutes : int, seconds : int, milliseconds : int) -> None:
        ms, msr = self.__calc(self.milliseconds + milliseconds, 1000)
        self.milliseconds = ms
        s, sr = self.__calc(self.seconds + seconds + msr, 60)
        self.seconds = s
        m, mr = self.__calc(self.minutes + minutes + sr, 60)
        self.minutes = m
        self.hours = self.hours + hours + mr

        self.assertvalid()

    def __calc(self, value : int, maxval : int) -> Tuple[int, int]:
        realval = value % maxval
        return (realval, value // maxval)

    @classmethod
    def fromstr(cls, timestr : str) -> Time:
        hour, minute, second, millisecond = re.split(':|,', timestr)
        return cls(hour, minute, second, millisecond)

    def assertvalid(self) -> None:
        assert abs(self.minutes) < 60, f'minutes: maximum value 60, actual {self.minutes}'
        assert abs(self.seconds) < 60, f'seconds: maximum value 60, actual {self.seconds}'
        assert abs(self.milliseconds) < 1000, f'milliseconds: maximum value 1000, actual {self.milliseconds}'
