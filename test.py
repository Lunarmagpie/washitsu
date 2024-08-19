from washitsu import *
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

pprint(
    Word(
        [
            syllable(
                segments,
                [select("b")],
                [],
                [],
            ),
        ]
    )
)
