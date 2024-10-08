from __future__ import annotations
import itertools
import copy
from dataclasses import dataclass
import random
import typing as t
from pprint import pprint

__all__ = [
    "Segment",
    "Word",
    "syllable",
    "Syllable",
    "ipa",
    "each_segment",
    "select",
    "find",
    "probability",
    "resyllabify",
    "syllabify_string",
    "_",
    "bilabial",
    "labiodental",
    "alveolar",
    "postalveolar",
    "retroflex",
    "palatal",
    "velar",
    "uvular",
    "pharyngeal",
    "glottal",
    "consonantal",
    "stop",
    "trill",
    "tap",
    "strident",
    "sibilant",
    "lateral",
    "voiced",
    "aspirated",
    "sonorant",
    "continuant",
    "nasal",
    "delayed_release",
    "syllabic",
    "front",
    "central",
    "back",
    "close",
    "near_close",
    "close_mid",
    "mid",
    "open_mid",
    "near_open",
    "open",
    "labialized",
    "palatalized",
    "velarized",
    "pharyngealized",
    "long",
    "optional",
    "repeat",
]


def lists_are_equal(a, b):
    return all(x in b for x in a) and all(x in a for x in b)


def subset_amount(a, b):
    amount = 0
    for item in a:
        if item not in b:
            amount += 1
    for item in b:
        if item not in a:
            amount += 1
    return amount


class HigherOrderFunction:
    def __init__(self, callable: t.Any) -> None:
        self.callable = callable
        self.name = callable.__name__

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

    def __and__(self, other):
        return all_combinator(self, other)

    def __or__(self, other):
        return any_combinator(self, other)

    def __xor__(self, other):
        return xor(self, other)

    def __neg__(self):
        return not_combinator(self)

    def __pos__(self):
        return self


def all_combinator(*argv):
    return HigherOrderFunction(lambda x: all(arg(x) for arg in argv))


def any_combinator(*argv):
    return HigherOrderFunction(lambda x: any(arg(x) for arg in argv))


def xor(left, right):
    return HigherOrderFunction(lambda x: left(x) ^ right(x))


def not_combinator(func):
    return HigherOrderFunction(lambda x: not func(x))


_ = HigherOrderFunction(lambda _: True)


class Feature(HigherOrderFunction):
    def __init__(self, name: str):
        super().__init__(self.has)
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name is other.name

    def has(self, x: list[Feature]):
        return self in x


# Place
bilabial = Feature("Bilabial")
labiodental = Feature("Labiodental")
alveolar = Feature("Alveolar")
postalveolar = Feature("PostAlveolar")
retroflex = Feature("Retroflex")
palatal = Feature("Palatal")
velar = Feature("Velar")
uvular = Feature("Uvular")
pharyngeal = Feature("Pharyngeal")
glottal = Feature("Glottal")
# Articulation
consonantal = Feature("Consonantal")
stop = Feature("Stop")
trill = Feature("Trill")
tap = Feature("Tap")
strident = Feature("Strident")
sibilant = Feature("Sibilant")
lateral = Feature("Lateral")
voiced = Feature("Voiced")
aspirated = Feature("Aspirated")
sonorant = Feature("Sonorant")
continuant = Feature("Continuant")
nasal = Feature("Nasal")
delayed_release = Feature("DelayedRelease")
# Vowels
syllabic = Feature("Syllabic")
front = Feature("Front")
central = Feature("Central")
back = Feature("Back")
close = Feature("Close")
near_close = Feature("NearClose")
close_mid = Feature("CloseMid")
mid = Feature("Mid")
open_mid = Feature("OpenMid")
near_open = Feature("NearOpen")
open = Feature("Open")
# Diacritic
labialized = Feature("Labialized")
palatalized = Feature("Palatalized")
velarized = Feature("Velarized")
pharyngealized = Feature("Pharyngealized")
long = Feature("Long")
# Special feature for syllabification
optional = Feature("Optional")
repeat = Feature("Repeat")

all_features = [
        bilabial,
    labiodental,
    alveolar,
    postalveolar,
    retroflex,
    palatal,
    velar,
    uvular,
    pharyngeal,
    glottal,
    consonantal,
    stop,
    trill,
    tap,
    strident,
    sibilant,
    lateral,
    voiced,
    aspirated,
    sonorant,
    continuant,
    nasal,
    delayed_release,
    syllabic,
    front,
    central,
    back,
    close,
    near_close,
    close_mid,
    mid,
    open_mid,
    near_open,
    open,
    labialized,
    palatalized,
    velarized,
    pharyngealized,
    long,
]

@dataclass
class Segment:
    ipa_symbol: str
    features: list[Feature]

    def __add__(self, other: Feature):
        changed = copy.copy(self)
        if other in self.features:
            return
        changed.features = copy.copy(self.features) + [other]
        return changed

    def __sub__(self, other: Feature):
        changed = copy.copy(self)
        changed.features = list(
            filter(lambda x: x is not other, copy.copy(self.features))
        )
        return changed

    def __eq__(self, other):
        return (
            isinstance(self, Segment)
            and isinstance(other, Segment)
            and self.ipa_symbol == other.ipa_symbol
            and lists_are_equal(self.features, other.features)
        )

    def has(self, feautres):
        return feautres(self.features)


SEGMENTS = [
    Segment("p", [consonantal, bilabial, stop]),
    Segment("b", [consonantal, bilabial, stop, voiced]),
    Segment("t", [consonantal, alveolar, stop]),
    Segment("d", [consonantal, alveolar, stop, voiced]),
    Segment("ʈ", [consonantal, retroflex, stop]),
    Segment("ɖ", [consonantal, retroflex, stop, voiced]),
    Segment("c", [consonantal, palatal, stop]),
    Segment("ɟ", [consonantal, palatal, stop, voiced]),
    Segment("k", [consonantal, velar, stop]),
    Segment("g", [consonantal, velar, stop, voiced]),
    Segment("q", [consonantal, uvular, stop]),
    Segment("ɢ", [consonantal, uvular, stop, voiced]),
    Segment("ʔ", [glottal, uvular, stop]),
    Segment("t͡s", [consonantal, alveolar, stop, delayed_release]),
    Segment("d͡z", [consonantal, alveolar, stop, voiced, delayed_release]),
    Segment("t͡ʃ", [consonantal, postalveolar, stop, delayed_release]),
    Segment("d͡ʒ", [consonantal, postalveolar, stop, voiced, delayed_release]),
    Segment("t͡ɕ", [consonantal, alveolar, palatal, stop, delayed_release]),
    Segment(
        "d͡ʑ",
        [consonantal, alveolar, palatal, stop, voiced, delayed_release],
    ),
    Segment("ʈ͡ʂ", [consonantal, retroflex, stop, delayed_release]),
    Segment("ɖ͡ʐ", [consonantal, retroflex, stop, voiced, delayed_release]),
    Segment(
        "t͡ɬ",
        [consonantal, alveolar, palatal, stop, lateral, delayed_release],
    ),
    Segment(
        "d͡ɮ",
        [consonantal, alveolar, palatal, stop, voiced, lateral, delayed_release],
    ),
    Segment("m̥", [consonantal, bilabial, stop, sonorant, nasal]),
    Segment("ɱ̊", [consonantal, labiodental, stop, sonorant, nasal]),
    Segment("n̥", [consonantal, alveolar, stop, sonorant, nasal]),
    Segment("ɳ̊", [consonantal, retroflex, stop, sonorant, nasal]),
    Segment("ɲ̊", [consonantal, palatal, stop, sonorant, nasal]),
    Segment("ŋ̊", [consonantal, velar, stop, sonorant, nasal]),
    Segment("ɴ̥", [consonantal, uvular, stop, sonorant, nasal]),
    Segment("m", [consonantal, bilabial, stop, sonorant, nasal, voiced]),
    Segment("ɱ", [consonantal, labiodental, stop, sonorant, nasal, voiced]),
    Segment("n", [consonantal, alveolar, stop, sonorant, nasal, voiced]),
    Segment("ɳ", [consonantal, retroflex, stop, sonorant, nasal, voiced]),
    Segment("ɲ", [consonantal, palatal, stop, sonorant, nasal, voiced]),
    Segment("ŋ", [consonantal, velar, stop, sonorant, nasal, voiced]),
    Segment("ɴ", [consonantal, uvular, stop, sonorant, nasal, voiced]),
    Segment("̥ʙ", [consonantal, bilabial, sonorant, continuant, trill]),
    Segment("̥r", [consonantal, alveolar, sonorant, continuant, trill]),
    Segment("̥ʀ", [consonantal, uvular, sonorant, continuant, trill]),
    Segment("̥ⱱ", [consonantal, labiodental, sonorant, continuant, tap]),
    Segment("̥ɾ", [consonantal, alveolar, sonorant, tap]),
    Segment("̊ɽ", [consonantal, retroflex, sonorant, tap]),
    Segment("ʙ", [consonantal, bilabial, sonorant, continuant, trill, voiced]),
    Segment("r", [consonantal, alveolar, sonorant, continuant, trill, voiced]),
    Segment("ʀ", [consonantal, uvular, sonorant, continuant, trill, voiced]),
    Segment("ⱱ", [consonantal, labiodental, sonorant, continuant, tap, voiced]),
    Segment("ɾ", [consonantal, alveolar, sonorant, tap, voiced]),
    Segment("ɽ", [consonantal, retroflex, sonorant, tap, voiced]),
    Segment("ɸ", [consonantal, continuant, bilabial, strident]),
    Segment("β", [consonantal, continuant, bilabial, strident, voiced]),
    Segment("f", [consonantal, continuant, labiodental, strident]),
    Segment("v", [consonantal, continuant, labiodental, strident, voiced]),
    Segment("θ", [consonantal, continuant, alveolar, strident]),
    Segment("ð", [consonantal, continuant, alveolar, strident, voiced]),
    Segment("s", [consonantal, continuant, alveolar, strident, sibilant]),
    Segment("z", [consonantal, continuant, alveolar, strident, sibilant, voiced]),
    Segment("ɬ", [consonantal, continuant, alveolar, strident, lateral]),
    Segment("ɮ", [consonantal, continuant, alveolar, strident, lateral, voiced]),
    Segment("ʃ", [consonantal, continuant, postalveolar, strident, sibilant]),
    Segment(
        "ʒ",
        [consonantal, continuant, postalveolar, strident, sibilant, voiced],
    ),
    Segment("ʂ", [consonantal, continuant, retroflex, strident, sibilant]),
    Segment(
        "ʐ",
        [consonantal, continuant, retroflex, strident, sibilant, voiced],
    ),
    Segment("ç", [consonantal, continuant, palatal, strident]),
    Segment("ʝ", [consonantal, continuant, palatal, strident, voiced]),
    Segment(
        "ɕ",
        [consonantal, continuant, alveolar, palatal, strident, sibilant],
    ),
    Segment(
        "ʑ",
        [consonantal, continuant, alveolar, palatal, strident, sibilant, voiced],
    ),
    Segment("x", [consonantal, continuant, velar, strident]),
    Segment("ɣ", [consonantal, continuant, velar, strident, voiced]),
    Segment("χ", [consonantal, continuant, uvular, strident]),
    Segment("ʁ", [consonantal, continuant, uvular, strident, voiced]),
    Segment("ħ", [consonantal, continuant, pharyngeal, strident]),
    Segment("ʕ", [consonantal, continuant, pharyngeal, strident, voiced]),
    Segment("h", [continuant, glottal, strident]),
    Segment("ɦ", [continuant, glottal, strident, voiced]),
    Segment("ʋ̥", [consonantal, continuant, sonorant, labiodental]),
    Segment("ɹ̥", [consonantal, continuant, sonorant, postalveolar]),
    Segment("ɻ̊", [consonantal, continuant, sonorant, retroflex]),
    Segment("ɰ̊", [continuant, sonorant, velar]),
    Segment("j̊", [continuant, sonorant, palatal]),
    Segment("ɥ̊", [continuant, sonorant, palatal, labialized]),
    Segment("ʍ", [continuant, sonorant, velar, labialized]),
    Segment("ʋ", [consonantal, continuant, sonorant, labiodental, voiced]),
    Segment("ɹ", [consonantal, continuant, sonorant, postalveolar, voiced]),
    Segment("ɻ", [consonantal, continuant, sonorant, retroflex, voiced]),
    Segment("ɰ", [continuant, sonorant, velar, voiced]),
    Segment("j", [continuant, sonorant, palatal, voiced]),
    Segment("ɥ", [continuant, sonorant, palatal, labialized, voiced]),
    Segment("w", [continuant, sonorant, velar, labialized, voiced]),
    Segment("l̥", [consonantal, continuant, sonorant, alveolar, lateral]),
    Segment("ɭ̊", [consonantal, continuant, sonorant, alveolar, lateral]),
    Segment("ʎ̥", [consonantal, continuant, sonorant, alveolar, lateral]),
    Segment("ʟ̥", [consonantal, continuant, sonorant, alveolar, lateral]),
    Segment("l", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    Segment("ɭ", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    Segment("ʎ", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    Segment("ʟ", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    # Vowels
    Segment("i̥", [syllabic, sonorant, front, close]),
    Segment("y̥", [syllabic, sonorant, front, labialized, close]),
    Segment("ɨ̥", [syllabic, sonorant, central, close]),
    Segment("ʉ̥", [syllabic, sonorant, central, labialized, close]),
    Segment("ɯ̥", [syllabic, sonorant, back, close]),
    Segment("u̥", [syllabic, sonorant, back, labialized, close]),
    Segment("ɪ̥", [syllabic, sonorant, front, near_close]),
    Segment("ʏ̥", [syllabic, sonorant, front, labialized, near_close]),
    Segment("ʊ̥", [syllabic, sonorant, back, labialized, near_close]),
    Segment("e̥", [syllabic, sonorant, front, close_mid]),
    Segment("ø̥", [syllabic, sonorant, front, labialized, close_mid]),
    Segment("ɘ̥", [syllabic, sonorant, central, close_mid]),
    Segment("ɵ̥", [syllabic, sonorant, central, labialized, close_mid]),
    Segment("ɤ̥", [syllabic, sonorant, back, close_mid]),
    Segment("o̥", [syllabic, sonorant, back, labialized, close_mid]),
    Segment("e̞̥", [syllabic, sonorant, front, mid]),
    Segment("ø̞̥", [syllabic, sonorant, front, labialized, mid]),
    Segment("ə̥", [syllabic, sonorant, central, mid]),
    Segment("ɤ̞̥", [syllabic, sonorant, back, mid]),
    Segment("o̞̥", [syllabic, sonorant, back, labialized, mid]),
    Segment("ɛ̥", [syllabic, sonorant, front, open_mid]),
    Segment("œ̥", [syllabic, sonorant, front, labialized, open_mid]),
    Segment("ɜ̥", [syllabic, sonorant, central, open_mid]),
    Segment("ɞ̥", [syllabic, sonorant, central, labialized, open_mid]),
    Segment("ʌ̥", [syllabic, sonorant, back, open_mid]),
    Segment("ɔ̥", [syllabic, sonorant, back, labialized, open_mid]),
    Segment("æ̥", [syllabic, sonorant, front, near_open]),
    Segment("ɐ̥", [syllabic, sonorant, central, near_open]),
    Segment("ḁ", [syllabic, sonorant, front, open]),
    Segment("ɶ̥", [syllabic, sonorant, front, labialized, open]),
    Segment("ḁ̈", [syllabic, sonorant, central, open]),
    Segment("ɑ̥", [syllabic, sonorant, back, open]),
    Segment("ɒ̥", [syllabic, sonorant, back, labialized, open]),
    Segment("y̥̑", [sonorant, front, labialized, close]),
    Segment("ɨ̯̥", [sonorant, central, close]),
    Segment("ʉ̯̥", [sonorant, central, labialized, close]),
    Segment("ɯ̯̥", [sonorant, back, close]),
    Segment("u̯̥", [sonorant, back, labialized, close]),
    Segment("ɪ̯̥", [sonorant, front, near_close]),
    Segment("ʏ̯̥", [sonorant, front, labialized, near_close]),
    Segment("ʊ̯̥", [sonorant, back, labialized, near_close]),
    Segment("e̯̥", [sonorant, front, close_mid]),
    Segment("ø̯̥", [sonorant, front, labialized, close_mid]),
    Segment("ɘ̯̥", [sonorant, central, close_mid]),
    Segment("ɵ̯̥", [sonorant, central, labialized, close_mid]),
    Segment("ɤ̯̥", [sonorant, back, close_mid]),
    Segment("o̯̥", [sonorant, back, labialized, close_mid]),
    Segment("i̯̥", [sonorant, front, close]),
    Segment("ȇ̞̥", [sonorant, front, mid]),
    Segment("ø̞̥̑", [sonorant, front, labialized, mid]),
    Segment("ə̯̥", [sonorant, central, mid]),
    Segment("ɤ̞̥̑", [sonorant, back, mid]),
    Segment("ȏ̞̥", [sonorant, back, labialized, mid]),
    Segment("ɛ̯̥", [sonorant, front, open_mid]),
    Segment("œ̯̥", [sonorant, front, labialized, open_mid]),
    Segment("ɜ̯̥", [sonorant, central, open_mid]),
    Segment("ɞ̯̥", [sonorant, central, labialized, open_mid]),
    Segment("ʌ̯̥", [sonorant, back, open_mid]),
    Segment("ɔ̯̥", [sonorant, back, labialized, open_mid]),
    Segment("æ̯̥", [sonorant, front, near_open]),
    Segment("ɐ̯̥", [sonorant, central, near_open]),
    Segment("a̯̥", [sonorant, front, open]),
    Segment("ɶ̯̥", [sonorant, front, labialized, open]),
    Segment("ä̯̥", [sonorant, central, open]),
    Segment("ɑ̯̥", [sonorant, back, open]),
    Segment("ɒ̯̥", [sonorant, back, labialized, open]),
    Segment("i", [syllabic, voiced, sonorant, front, close]),
    Segment("y", [syllabic, voiced, sonorant, front, labialized, close]),
    Segment("ɨ", [syllabic, voiced, sonorant, central, close]),
    Segment("ʉ", [syllabic, voiced, sonorant, central, labialized, close]),
    Segment("ɯ", [syllabic, voiced, sonorant, back, close]),
    Segment("u", [syllabic, voiced, sonorant, back, labialized, close]),
    Segment("ɪ", [syllabic, voiced, sonorant, front, near_close]),
    Segment("ʏ", [syllabic, voiced, sonorant, front, labialized, near_close]),
    Segment("ʊ", [syllabic, voiced, sonorant, back, labialized, near_close]),
    Segment("e", [syllabic, voiced, sonorant, front, close_mid]),
    Segment("ø", [syllabic, voiced, sonorant, front, labialized, close_mid]),
    Segment("ɘ", [syllabic, voiced, sonorant, central, close_mid]),
    Segment("ɵ", [syllabic, voiced, sonorant, central, labialized, close_mid]),
    Segment("ɤ", [syllabic, voiced, sonorant, back, close_mid]),
    Segment("o", [syllabic, voiced, sonorant, back, labialized, close_mid]),
    Segment("e̞", [syllabic, voiced, sonorant, front, mid]),
    Segment("ø̞", [syllabic, voiced, sonorant, front, labialized, mid]),
    Segment("ə", [syllabic, voiced, sonorant, central, mid]),
    Segment("ɤ̞", [syllabic, voiced, sonorant, back, mid]),
    Segment("o̞", [syllabic, voiced, sonorant, back, labialized, mid]),
    Segment("ɛ", [syllabic, voiced, sonorant, front, open_mid]),
    Segment("œ", [syllabic, voiced, sonorant, front, labialized, open_mid]),
    Segment("ɜ", [syllabic, voiced, sonorant, central, open_mid]),
    Segment("ɞ", [syllabic, voiced, sonorant, central, labialized, open_mid]),
    Segment("ʌ", [syllabic, voiced, sonorant, back, open_mid]),
    Segment("ɔ", [syllabic, voiced, sonorant, back, labialized, open_mid]),
    Segment("æ", [syllabic, voiced, sonorant, front, near_open]),
    Segment("ɐ", [syllabic, voiced, sonorant, central, near_open]),
    Segment("a", [syllabic, voiced, sonorant, front, open]),
    Segment("ɶ", [syllabic, voiced, sonorant, front, labialized, open]),
    Segment("ä", [syllabic, voiced, sonorant, central, open]),
    Segment("ɑ", [syllabic, voiced, sonorant, back, open]),
    Segment("ɒ", [syllabic, voiced, sonorant, back, labialized, open]),
    Segment("i̯", [voiced, sonorant, front, close]),
    Segment("y̑", [voiced, sonorant, front, labialized, close]),
    Segment("ɨ̯", [voiced, sonorant, central, close]),
    Segment("ʉ̯", [voiced, sonorant, central, labialized, close]),
    Segment("ɯ̯", [voiced, sonorant, back, close]),
    Segment("u̯", [voiced, sonorant, back, labialized, close]),
    Segment("ɪ̯", [voiced, sonorant, front, near_close]),
    Segment("ʏ̯", [voiced, sonorant, front, labialized, near_close]),
    Segment("ʊ̯", [voiced, sonorant, back, labialized, near_close]),
    Segment("e̯", [voiced, sonorant, front, close_mid]),
    Segment("ø̯", [voiced, sonorant, front, labialized, close_mid]),
    Segment("ɘ̯", [voiced, sonorant, central, close_mid]),
    Segment("ɵ̯", [voiced, sonorant, central, labialized, close_mid]),
    Segment("ɤ̯", [voiced, sonorant, back, close_mid]),
    Segment("o̯", [voiced, sonorant, back, labialized, close_mid]),
    Segment("ȇ̞", [voiced, sonorant, front, mid]),
    Segment("ø̞̑", [voiced, sonorant, front, labialized, mid]),
    Segment("ə̯", [voiced, sonorant, central, mid]),
    Segment("ɤ̞̑", [voiced, sonorant, back, mid]),
    Segment("ȏ̞", [voiced, sonorant, back, labialized, mid]),
    Segment("ɛ̯", [voiced, sonorant, front, open_mid]),
    Segment("œ̯", [voiced, sonorant, front, labialized, open_mid]),
    Segment("ɜ̯", [voiced, sonorant, central, open_mid]),
    Segment("ɞ̯", [voiced, sonorant, central, labialized, open_mid]),
    Segment("ʌ̯", [voiced, sonorant, back, open_mid]),
    Segment("ɔ̯", [voiced, sonorant, back, labialized, open_mid]),
    Segment("æ̯", [voiced, sonorant, front, near_open]),
    Segment("ɐ̯", [voiced, sonorant, central, near_open]),
    Segment("a̯", [voiced, sonorant, front, open]),
    Segment("ɶ̯", [voiced, sonorant, front, labialized, open]),
    Segment("ä̯", [voiced, sonorant, central, open]),
    Segment("ɑ̯", [voiced, sonorant, back, open]),
    Segment("ɒ̯", [voiced, sonorant, back, labialized, open]),
]

DIACRITICS = [
    Segment("ˠ", [velarized]),
    Segment("ˤ", [pharyngealized]),
    Segment("ʷ", [labialized]),
    Segment("ʲ", [palatalized]),
    Segment("ʰ", [aspirated]),
    Segment("̃", [nasal]),
    Segment("ː", [long]),
    Segment("R", [repeat]),
    Segment("O", [optional]),
]


def ipa(*symbols: list[str]) -> list[Segment]:
    output: list[Segment] = []
    for symbol in symbols:
        extra_features = []
        for diacritic in DIACRITICS:
            if diacritic.ipa_symbol in symbol:
                extra_features += diacritic.features

        segment = next(filter(lambda s: s.ipa_symbol in symbol, SEGMENTS))
        new_segment = Segment(symbol, segment.features + extra_features)
        output.append(new_segment)
    return output


def syllable(
    segments: list[Segment],
    onset: list[t.Callable[[list[Feature]], bool] | None],
    nucleus: list[t.Callable[[list[Feature]], bool] | None],
    coda: list[t.Callable[[list[Feature]], bool] | None],
):
    output = []

    for segment in [onset, nucleus, coda]:
        outputoutput = []

        for segmentsegment in segment:
            if not segmentsegment:
                continue
            stuff = list(filter(lambda x: segmentsegment(x.features), segments))
            outputoutput += [random.choice(stuff)]

        output += [outputoutput]

    return Syllable(*output)


@dataclass
class Syllable:
    onset: list[Segment]
    nucleus: list[Segment]
    coda: list[Segment]

    # supersegmentals: list[Feature]
    #
    def __eq__(self, other):
        return (
            lists_are_equal(self.onset, other.onset)
            and lists_are_equal(self.nucleus, other.nucleus)
            and lists_are_equal(self.coda, other.coda)
        )


def _default_word_printer(segment: Segment) -> str:
    subset_amounts = []
    for big_seg in SEGMENTS:
        subset_amounts += [(big_seg, subset_amount(segment.features, big_seg.features))]

    subset_amounts: list[tuple[Segment, int]] = sorted(
        subset_amounts, key=lambda x: x[1]
    )

    chosen_seg = subset_amounts[0][0]
    leftover_features = copy.copy(segment.features)
    for feature in chosen_seg.features:
        if feature in leftover_features:
            leftover_features.remove(feature)

    diacritics = ""

    for feature in leftover_features:
        try:
            diacritics += next(
                filter(lambda x: x.features == [feature], DIACRITICS)
            ).ipa_symbol
        except:
            raise Exception(f"Can not find matching segment: {segment.features}")

    return subset_amounts[0][0].ipa_symbol + diacritics


def each_segment(f: t.Callable[[Word], Segment | list[Segment]]):
    def out(word):
        syllables = []

        def to_list(x):
            if isinstance(x, list):
                return x
            else:
                return [x]

        for syllable in word.syllables:
            onset = list(
                itertools.chain(
                    *map(to_list, map(lambda s: f(word, s), syllable.onset))
                )
            )
            nucleus = list(
                itertools.chain(
                    *map(to_list, map(lambda s: f(word, s), syllable.nucleus))
                )
            )
            coda = list(
                itertools.chain(*map(to_list, map(lambda s: f(word, s), syllable.coda)))
            )

            syllables.append(Syllable(onset, nucleus, coda))

        return Word(syllables)

    return out


def syllabify(
    segments,
    onset: list[HigherOrderFunction],
    nucleus: list[HigherOrderFunction],
    coda: list[HigherOrderFunction],
):
    def get_syllable_section(index: int) -> str:
        if index < len(onset):
            return "onset"
        if index < len(onset) + len(nucleus):
            return "nucleus"
        return "coda"

    def push_to_last(segment: Segment, index: int, syllables: list[Syllable]):
        section = get_syllable_section(index)
        if section == "onset":
            syllables[len(syllables) - 1].onset.append(segment)
        if section == "nucleus":
            syllables[len(syllables) - 1].nucleus.append(segment)
        if section == "coda":
            syllables[len(syllables) - 1].coda.append(segment)
        return syllables

    syllables = []

    index = 0
    letter_index = 0
    structure_list = onset + nucleus + coda
    syllables.append(Syllable([], [], []))

    while letter_index < len(segments):
        segment = segments[letter_index]
        check = structure_list[index]
        prev_index = (index - 1) % len(structure_list)
        prev_check = structure_list[prev_index]

        features = segment.features + [optional] + [repeat]

        if check(features):
            syllables = push_to_last(segment, index, syllables)
            letter_index += 1
        elif prev_check(all_features + [repeat]) & prev_check(features):
            last_syllable = syllables[len(syllables) - 1]
            if len(last_syllable.onset + last_syllable.nucleus + last_syllable.coda) == 0:
                syllables.pop()
            syllables = push_to_last(segment, prev_index, syllables)
            letter_index += 1
            index -= 1
        elif check([optional]):
            pass
        else:
            raise Exception(f"Invalid Syllable structure: {syllables}")

        if index == len(structure_list) - 1 and letter_index < len(segments):
            syllables.append(Syllable([], [], []))
            index = 0
        else:
            index += 1

    return Word(syllables)


def syllabify_string(
    string: str,
    onset: list[HigherOrderFunction],
    nucleus: list[HigherOrderFunction],
    coda: list[HigherOrderFunction],
):
    out = []
    for s in string:
        out.append(find(s))
    return syllabify(out, onset, nucleus, coda)


def resyllabify(
    onset: list[HigherOrderFunction],
    nucleus: list[HigherOrderFunction],
    coda: list[HigherOrderFunction],
):
    def wrap(f: t.Callable[[Word], any]):
        def out(word: Word):
            segments = word.flatten()
            return syllabify(segments, onset, nucleus, coda)

        return out

    return wrap


@dataclass
class Word:
    syllables: list[Syllable]

    def show(self, printer: t.Callable[[Segment], str] = _default_word_printer) -> None:
        output = []
        for syllable in self.syllables:
            output += (
                "".join(
                    [
                        printer(x)
                        for x in [*syllable.onset, *syllable.nucleus, *syllable.coda]
                    ]
                )
                + "."
            )
        print("".join(output))
        return self

    def flatten(self) -> list[Segment]:
        segments = []

        for syllable in self.syllables:
            segments += [*syllable.onset, *syllable.nucleus, *syllable.coda]

        return segments

    @t.overload
    def matches(self, before: list, segment: Segment, after: list) -> bool: ...

    @t.overload
    def matches(self, before: list, segment: Segment) -> bool: ...

    @t.overload
    def matches(self, segment: Segment, after: list) -> bool: ...

    @t.overload
    def matches(self, segment: Segment) -> bool: ...

    def matches(self, *args):
        if len(args) == 3:
            return self._matches(args[0], args[1], args[2])

        if len(args) == 2 and isinstance(args[0], Segment):
            return self._matches([], args[0], args[1])

        if len(args) == 2 and isinstance(args[1], Segment):
            return self._matches(args[0], args[1], [])

        if len(args) == 1:
            return self._matches([], args[0], [])

        raise Exception("Unknown overload")

    def _matches(self, before, syllable, after):
        syllables = self.flatten()
        index = syllables.index(syllable)

        if (index - len(before)) < 0:
            return False

        if (index + len(after)) >= len(syllables):
            return False

        before_part = syllables[index - len(before) : index]
        after_part = syllables[index + 1 : index + 1 + len(after)]

        def matches(parts, funcs):
            if len(funcs) == 0:
                return True
            return all(b(a.features) for (a, b) in zip(parts, funcs))

        if not matches(before_part, before):
            return False

        if not matches(after_part, after):
            return False

        return True

    def then(self, sound_change: t.Callable[[Word], Word]) -> t.Self:
        return sound_change(self)

    def _includes(self, search: HigherOrderFunction, list: list[Feature]) -> bool:
        """
        Find if a Feature exists in a list of Features.
        """
        for segment in list:
            result = search(segment.features)
            if result == True:
                return True
        return False

    def includes(self, includes: HigherOrderFunction) -> bool:
        """
        Find if a segment with the features given exists within a word.
        """
        flattenedSegments = self.flatten()
        return self._includes(includes, flattenedSegments)

    def includes_before(self, segment: Segment, includes: HigherOrderFunction) -> bool:
        """
        Find if a segment with the features given exists within a word, before another segment.
        """
        flattenedSegments = self.flatten()
        index = flattenedSegments.index(segment)
        return self._includes(includes, flattenedSegments[index:])

    def includes_after(self, segment: Segment, includes: HigherOrderFunction) -> bool:
        """
        Find if a segment with the features given exists within a word, after another segment.
        """
        flattenedSegments = self.flatten()
        index = flattenedSegments.index(segment)
        return self._includes(includes, flattenedSegments[:index])

    def first(self, segment: Segment) -> bool:
        """
        Find if a segment is the first segment in a word.
        """
        flattenedSegments = self.flatten()
        return self._includes(flattenedSegments.index(segment) == 0)

    def last(self, segment: Segment) -> bool:
        """
        Find if a segment is the last segment in a word.
        """
        flattenedSegments = self.flatten()
        return self._includes(
            flattenedSegments.index(segment) == len(flattenedSegments) - 1
        )


def merge(features: list[Feature]) -> HigherOrderFunction:
    output = features[0]
    for i in range(0, len(features) - 1):
        next_feature = features[i + 1]
        output = output & next_feature
    return output


def select(symbol: str) -> Feature:
    features = ipa(symbol)[0].features
    full_features = list(itertools.chain.from_iterable([s.features for s in SEGMENTS]))
    all_features: list[Feature] = []
    [all_features.append(x) for x in full_features if x not in all_features]

    output = features[0]
    for i in range(0, len(all_features) - 1):
        next_feature = all_features[i + 1]
        if next_feature in features:
            output = output & next_feature
        else:
            output = output & -next_feature

    return output


def find(symbol: str) -> Segment:
    return next(filter(lambda x: x.ipa_symbol == symbol, SEGMENTS))


def probability(feature: Feature, chance: float):
    if chance > random.random():
        return feature
