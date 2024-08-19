from washitsu import *
from washitsu.rules import *
from pprint import pprint


segments = ipa(
    "m",
    "n",
    # "pʰ",
    # "tʰ",
    # "kʰ",
    # "kʷʰ",
    "p",
    "t",
    "k",
    # "kʷ",
    "b",
    "d",
    "g",
    # "gʷ",
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
            [select("g")],
            [select("a")],
            [select("p")],
        ),
        syllable(
            segments,
            [select("b")],
            [select("u")],
            [],
        ),
    ]
).show().then(each_segment(voicing_assim)).show()
