from washitsu import *
from washitsu import _
from pprint import pprint


segments = ipa(
    "m",
    "n",
    "pʰ",
    "tʰ",
    "kʰ",
    "kʷʰ",
    "p",
    "t",
    "k",
    "kʷ",
    "b",
    "d",
    "g",
    "gʷ",
    "s",
    "x",
    "h",
    "l",
    "r",
    "j",
    "w",
    "i",
    "u",
    "e",
    "o",
    "a",
    "ə",
)


def voicing_assim(word: Word, segment: Segment) -> Segment:
    if word.surrounds([], segment, [voiced & consonantal]):
        return segment + voiced
    return segment



def show(a):
    return str(a.features)

Word(
    [
        syllable(
            segments,
            [strident & (alveolar | glottal), -strident & -voiced & -aspirated, +trill],
            [+syllabic],
            [+consonantal],
        ),
        syllable(
            segments,
            [consonantal],
            [syllabic],
            [consonantal],
        ),
    ]
).show(show).then(each_segment(voicing_assim)).show(show)
