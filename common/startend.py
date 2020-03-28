from __future__ import annotations
from common.time import Time

class StartEnd:
    def __init__(self, start : Time, end : Time):
        self.start = start
        self.end   = end

    def __str__(self):
        return f'{str(self.start)} {self.time_separator()} {str(self.end)}\n'

    def __repr__(self):
        return str(self)

    @classmethod
    def fromstr(cls, startendstr : str) -> StartEnd:
        s, e = startendstr.split(cls.time_separator(), 1)
        return cls(Time.fromstr(s.strip()), Time.fromstr(e.strip()))

    @staticmethod
    def time_separator() -> str:
        return '-->'

    def add(self, diff : Time) -> None:
        self.start = self.start.add(diff)
        self.end   = self.end.add(diff)
