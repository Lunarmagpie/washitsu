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
).show()
