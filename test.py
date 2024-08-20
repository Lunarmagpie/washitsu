from washitsu import *
from washitsu.rules import *
from pprint import pprint
import random


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

(
    Word(
        [
            syllable(segments, [select("m")], [select("u")], [select("s")]),
        ]
    )
    .show()
    .then(umlaut)
    .show()
    .then(great_vowel_shift)
    .show()
)
