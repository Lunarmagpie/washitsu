from __future__ import annotations
from washitsu import *

obstruent = -sonorant


def voicing_assim(word: Word, segment: Segment) -> Segment:
    if word.surrounds([], segment, [voiced & consonantal & obstruent]) and segment.has(
        consonantal & obstruent
    ):
        return segment + voiced
    if word.surrounds([], segment, [-voiced & consonantal & obstruent]) and segment.has(
        consonantal & obstruent
    ):
        return segment - voiced
    return segment


def intervocalic_voicing(word: Word, segment: Segment) -> Segment:
    if word.surrounds(
        [voiced & -consonantal], segment, [voiced & -consonantal]
    ) and segment.has(consonantal & obstruent):
        return segment + voiced
    return segment


def rhoticization(word: Word, segment: Segment) -> Segment:
    if segment.has(select("z")):
        segment.features += [select("r")]
        return segment
    return segment
