from washitsu import *
from washitsu.rules import *
import random

segments = ipa(
    "i",
    "u",
    "e",
    "u",
    "o",
    "a",
    "m",
    "n",
    "p",
    "k",
    "ʔ",
    "h",
    "w",
    "l",
)

for i in range(0, 10):
    word_length = random.randint(1, 5)
    (
        Word(
            [
                a(
                    segments,
                    [probability(-syllabic, 0.8)],
                    [+syllabic],
                    [],
                )
                for a in [syllable] * word_length
            ]
        ).show()
    )
