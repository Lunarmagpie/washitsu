from __future__ import annotations

from washitsu import *

def voicing_assim(word: Word, segment: Segment) -> Segment:
    if word.surrounds([], segment, [voiced & consonantal]) and segment.has(consonantal):
        return segment + voiced
    return segment

