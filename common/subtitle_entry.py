from __future__ import annotations
from typing import NamedTuple

from common.startend import StartEnd

SubtitleEntry = NamedTuple('SubtitleEntry',
        [('number', int), ('start_end', StartEnd), ('content', str)])
