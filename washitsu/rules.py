from __future__ import annotations

def voicing_assim(word: Word, segment: Segment) -> Segment:
    if word.surrounds([], segment, [voiced & consonantal]) and segment.has(consonantal):
        return segment + voiced
    return segment

