from typing import List
from itertools import groupby

from common.subtitle_entry import SubtitleEntry
from common.startend import StartEnd

class SrtFileHandler:

    @classmethod
    def parsesrt(cls, filename : str) -> List[SubtitleEntry]:
        with open(filename) as f:
             entries = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]
        parsedentries = []

        for entry in entries:
            number, start_end, *content = entry
            parsed_entry = SubtitleEntry(number, StartEnd.fromstr(start_end), ''.join(content))
            parsedentries.append(parsed_entry)
        return parsedentries

    @classmethod
    def writesrt(cls, entries : List[SubtitleEntry], filename : str) -> None:
        xs = [ cls.formatentry(x) for x in entries ]
        with open(filename, 'w') as f:
            f.writelines(xs)

    @classmethod
    def formatentry(cls, entry : SubtitleEntry) -> str:
        return ''.join(list((entry.number, str(entry.start_end), entry.content, '\n')))


