from __future__ import annotations
from washitsu import *

obstruent = -sonorant

@each_segment
def voicing_assim(word: Word, segment: Segment) -> Segment:
    if word.matches(segment, [voiced & consonantal & obstruent]) and segment.has(
        consonantal & obstruent
    ):
        return segment + voiced
    if word.matches(segment, [-voiced & consonantal & obstruent]) and segment.has(
        consonantal & obstruent
    ):
        return segment - voiced
    return segment


@each_segment
def intervocalic_voicing(word: Word, segment: Segment) -> Segment:
    if word.matches(
        [voiced & -consonantal], segment, [voiced & -consonantal]
    ) and segment.has(consonantal & obstruent):
        return segment + voiced
    return segment


@each_segment
def rhoticization(word: Word, segment: Segment) -> Segment:
    if segment.has(select("z")):
        return find("r")
    return segment


@each_segment
def gnarsh_chain_shift(word: Word, segment: Segment) -> Segment:
    if segment.has(select("i")):
        return segment - front + back
    if segment.has(select("u")):
        return segment - close + close_mid
    if segment.has(select("e")):
        return segment - close_mid + close
    if segment.has(select("o")):
        return segment - close_mid + open
    if segment.has(select("a")):
        return segment - open + close_mid
    return segment


@each_segment
def umlaut(word: Word, segment: Segment) -> Segment:
    if word.includes_before(segment, close & front) and segment.has(back):
        return segment - back + front
    return segment


@each_segment
def great_vowel_shift(word: Word, segment: Segment) -> Segment:
    if segment.has(close):
        return [find("a"), segment - syllabic]
    if segment.has(close_mid):
        return segment - close_mid + close
    return segment
