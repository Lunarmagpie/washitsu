from washitsu import *
from washitsu.rules import *
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

(
    Word(
        [
            syllable(
                segments,
                [
                    strident & (alveolar | glottal),
                    -strident & -voiced & -aspirated,
                    +trill,
                ],
                [syllabic],
                [],
            ),
            syllable(
                segments,
                [select("s")],
                [syllabic],
                [],
            ),
        ]
    )
    .show()
    .then(each_segment(gnarsh_chain_shift))
    .show()
)
