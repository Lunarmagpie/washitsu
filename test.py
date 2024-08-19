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

for i in range(0, 10):
    word_length = random.randint(1, 3)
    (
        Word(
            [a(segments,
                random.choice([[
                    strident & (alveolar | glottal),
                    -strident & -voiced & -aspirated,
                    probability(+trill | +lateral, 0.4),
                ], [probability(-syllabic, 0.8)]]),
                [syllabic],
                [probability(-syllabic, 0.5), probability(-syllabic & -sonorant, 0.5)],
            ) for a in [syllable] * word_length]
        )
        .then(each_segment(voicing_assim))
        .show()
    )
