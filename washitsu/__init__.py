from __future__ import annotations

from dataclasses import dataclass
import typing as t
import random
import copy
import builtins


def lists_are_equal(a, b):
    return all(a == b for (a, b) in zip(a.sort(), b.sort()))


class HigherOrderFunction:
    def __init__(self, callable: t.Any) -> None:
        self.callable = callable

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

    def __and__(self, other):
        return all(self, other)

    def __or__(self, other):
        return any(self, other)

    def __neg__(self):
        return not_combinator(self)

    def __pos__(self):
        return self


def all(*argv):
    return HigherOrderFunction(lambda x: builtins.all(arg(x) for arg in argv))


def any(*argv):
    return HigherOrderFunction(lambda x: builtins.any(arg(x) for arg in argv))


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
stop = Feature("stop")
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
high = Feature("high")
mid_high = Feature("Midhigh")
low = Feature("Low")
back = Feature("back")
tense = Feature("Tense")
labialized = Feature("Labialized")


@dataclass
class Segment:
    ipa_symbol: str
    features: list[Feature]

    def __add__(self, other: Feature):
        changed = copy.deepcopy(self)
        changed.features += [other]
        return changed

    def __eq__(self, other):
        return (
            isinstance(self, Segment)
            and isinstance(other, Segment)
            and self.ipa_symbol == other.ipa_symbol
            and lists_are_equal(self.features, other.features)
        )


SEGMENT_PRINTING_TABLE = [
    ("p", [consonantal, bilabial, stop]),
    ("b", [consonantal, bilabial, stop, voiced]),
    ("t", [consonantal, alveolar, stop]),
    ("d", [consonantal, alveolar, stop, voiced]),
    ("ʈ", [consonantal, retroflex, stop]),
    ("ɖ", [consonantal, retroflex, stop, voiced]),
    ("c", [consonantal, palatal, stop]),
    ("ɟ", [consonantal, palatal, stop, voiced]),
    ("k", [consonantal, velar, stop]),
    ("g", [consonantal, velar, stop, voiced]),
    ("q", [consonantal, uvular, stop]),
    ("ɢ", [consonantal, uvular, stop, voiced]),
    ("ʔ", [glottal, uvular, stop]),
    ("t͡s", [consonantal, alveolar, stop, delayed_release]),
    ("d͡z", [consonantal, alveolar, stop, voiced, delayed_release]),
    ("t͡ʃ", [consonantal, postalveolar, stop, delayed_release]),
    ("d͡ʒ", [consonantal, postalveolar, stop, voiced, delayed_release]),
    ("t͡ɕ", [consonantal, alveolar, palatal, stop, delayed_release]),
    (
        "d͡ʑ",
        [consonantal, alveolar, palatal, stop, voiced, delayed_release],
    ),
    ("ʈ͡ʂ", [consonantal, retroflex, stop, delayed_release]),
    ("ɖ͡ʐ", [consonantal, retroflex, stop, voiced, delayed_release]),
    (
        "t͡ɬ",
        [consonantal, alveolar, palatal, stop, lateral, delayed_release],
    ),
    (
        "d͡ɮ",
        [consonantal, alveolar, palatal, stop, voiced, lateral, delayed_release],
    ),
    ("m̥", [consonantal, bilabial, stop, sonorant, nasal]),
    ("ɱ̊", [consonantal, labiodental, stop, sonorant, nasal]),
    ("n̥", [consonantal, alveolar, stop, sonorant, nasal]),
    ("ɳ̊", [consonantal, retroflex, stop, sonorant, nasal]),
    ("ɲ̊", [consonantal, palatal, stop, sonorant, nasal]),
    ("ŋ̊", [consonantal, velar, stop, sonorant, nasal]),
    ("ɴ̥", [consonantal, uvular, stop, sonorant, nasal]),
    ("m", [consonantal, bilabial, stop, sonorant, nasal, voiced]),
    ("ɱ", [consonantal, labiodental, stop, sonorant, nasal, voiced]),
    ("n", [consonantal, alveolar, stop, sonorant, nasal, voiced]),
    ("ɳ", [consonantal, retroflex, stop, sonorant, nasal, voiced]),
    ("ɲ", [consonantal, palatal, stop, sonorant, nasal, voiced]),
    ("ŋ", [consonantal, velar, stop, sonorant, nasal, voiced]),
    ("ɴ", [consonantal, uvular, stop, sonorant, nasal, voiced]),
    ("̥ʙ", [consonantal, bilabial, sonorant, continuant, trill]),
    ("̥r", [consonantal, alveolar, sonorant, continuant, trill]),
    ("̥ʀ", [consonantal, uvular, sonorant, continuant, trill]),
    ("̥ⱱ", [consonantal, labiodental, sonorant, continuant, tap]),
    ("̥ɾ", [consonantal, alveolar, sonorant, tap]),
    ("̊ɽ", [consonantal, retroflex, sonorant, tap]),
    ("ʙ", [consonantal, bilabial, sonorant, continuant, trill, voiced]),
    ("r", [consonantal, alveolar, sonorant, continuant, trill, voiced]),
    ("ʀ", [consonantal, uvular, sonorant, continuant, trill, voiced]),
    ("ⱱ", [consonantal, labiodental, sonorant, continuant, tap, voiced]),
    ("ɾ", [consonantal, alveolar, sonorant, tap, voiced]),
    ("ɽ", [consonantal, retroflex, sonorant, tap, voiced]),
    ("ɸ", [consonantal, continuant, bilabial, strident]),
    ("β", [consonantal, continuant, bilabial, strident, voiced]),
    ("f", [consonantal, continuant, labiodental, strident]),
    ("v", [consonantal, continuant, labiodental, strident, voiced]),
    ("θ", [consonantal, continuant, alveolar, strident]),
    ("ð", [consonantal, continuant, alveolar, strident, voiced]),
    ("s", [consonantal, continuant, alveolar, strident, sibilant]),
    ("z", [consonantal, continuant, alveolar, strident, sibilant, voiced]),
    ("ɬ", [consonantal, continuant, alveolar, strident, lateral]),
    ("ɮ", [consonantal, continuant, alveolar, strident, lateral, voiced]),
    ("ʃ", [consonantal, continuant, postalveolar, strident, sibilant]),
    (
        "ʒ",
        [consonantal, continuant, postalveolar, strident, sibilant, voiced],
    ),
    ("ʂ", [consonantal, continuant, retroflex, strident, sibilant]),
    (
        "ʐ",
        [consonantal, continuant, retroflex, strident, sibilant, voiced],
    ),
    ("ç", [consonantal, continuant, palatal, strident]),
    ("ʝ", [consonantal, continuant, palatal, strident, voiced]),
    (
        "ɕ",
        [consonantal, continuant, alveolar, palatal, strident, sibilant],
    ),
    (
        "ʑ",
        [consonantal, continuant, alveolar, palatal, strident, sibilant, voiced],
    ),
    ("x", [consonantal, continuant, velar, strident]),
    ("ɣ", [consonantal, continuant, velar, strident, voiced]),
    ("χ", [consonantal, continuant, uvular, strident]),
    ("ʁ", [consonantal, continuant, uvular, strident, voiced]),
    ("ħ", [consonantal, continuant, pharyngeal, strident]),
    ("ʕ", [consonantal, continuant, pharyngeal, strident, voiced]),
    ("h", [continuant, glottal, strident]),
    ("ɦ", [continuant, glottal, strident, voiced]),
    ("ʋ̥", [consonantal, continuant, sonorant, labiodental]),
    ("ɹ̥", [consonantal, continuant, sonorant, postalveolar]),
    ("ɻ̊", [consonantal, continuant, sonorant, retroflex]),
    ("ɰ̊", [continuant, sonorant, velar]),
    ("j̊", [continuant, sonorant, palatal]),
    ("ɥ̊", [continuant, sonorant, palatal, labialized]),
    ("ʍ", [continuant, sonorant, velar, labialized]),
    ("ʋ", [consonantal, continuant, sonorant, labiodental, voiced]),
    ("ɹ", [consonantal, continuant, sonorant, postalveolar, voiced]),
    ("ɻ", [consonantal, continuant, sonorant, retroflex, voiced]),
    ("ɰ", [continuant, sonorant, velar, voiced]),
    ("j", [continuant, sonorant, palatal, voiced]),
    ("ɥ", [continuant, sonorant, palatal, labialized, voiced]),
    ("w", [continuant, sonorant, velar, labialized, voiced]),
    ("l̥", [consonantal, continuant, sonorant, alveolar, lateral]),
    ("ɭ̊", [consonantal, continuant, sonorant, alveolar, lateral]),
    ("ʎ̥", [consonantal, continuant, sonorant, alveolar, lateral]),
    ("ʟ̥", [consonantal, continuant, sonorant, alveolar, lateral]),
    ("l", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    ("ɭ", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    ("ʎ", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    ("ʟ", [consonantal, continuant, sonorant, alveolar, lateral, voiced]),
    ("ɪ", [syllabic, voiced, sonorant, continuant, high]),
    ("ʊ", [syllabic, voiced, sonorant, continuant, high, back, labialized]),
    ("ɛ", [syllabic, voiced, sonorant, continuant, mid_high]),
    ("ɔ", [syllabic, voiced, sonorant, continuant, mid_high, back, labialized]),
    ("ɐ", [syllabic, voiced, sonorant, continuant, low]),
    ("i", [syllabic, voiced, sonorant, continuant, high, tense]),
    ("u", [syllabic, voiced, sonorant, continuant, high, back, labialized, tense]),
    ("e", [syllabic, voiced, sonorant, continuant, mid_high, tense]),
    ("o", [syllabic, voiced, sonorant, continuant, mid_high, back, labialized, tense]),
    ("a", [syllabic, voiced, sonorant, continuant, low, tense]),
    ("ə", [syllabic, voiced, sonorant, continuant]),
]

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
    Segment("ɪ", [syllabic, voiced, sonorant, continuant, high]),
    Segment("ʊ", [syllabic, voiced, sonorant, continuant, high, back, labialized]),
    Segment("ɛ", [syllabic, voiced, sonorant, continuant, mid_high]),
    Segment("ɔ", [syllabic, voiced, sonorant, continuant, mid_high, back, labialized]),
    Segment("ɐ", [syllabic, voiced, sonorant, continuant, low]),
    Segment("i", [syllabic, voiced, sonorant, continuant, high, tense]),
    Segment(
        "u", [syllabic, voiced, sonorant, continuant, high, back, labialized, tense]
    ),
    Segment("e", [syllabic, voiced, sonorant, continuant, mid_high, tense]),
    Segment(
        "o", [syllabic, voiced, sonorant, continuant, mid_high, back, labialized, tense]
    ),
    Segment("a", [syllabic, voiced, sonorant, continuant, low, tense]),
    Segment("ə", [syllabic, voiced, sonorant, continuant]),
]


def ipa(*symbols: list[str]):
    output = []
    for symbol in symbols:
        extra_features = []
        if "ʰ" in symbol:
            extra_features.append(aspirated)
        if "ʷ" in symbol:
            extra_features.append(labialized)

        segment = next(filter(lambda s: s.ipa_symbol in symbol, SEGMENTS))
        new_segment = Segment(symbol, segment.features + extra_features)
        output.append(new_segment)
    return output


def syllable(
    segments: list[Segment],
    onset: list[t.Callable[[list[Feature]], bool]],
    nucleus: list[t.Callable[[list[Feature]], bool]],
    coda: list[t.Callable[[list[Feature]], bool]],
):
    output = []

    for segment in [onset, nucleus, coda]:
        outputoutput = []

        for segmentsegment in segment:
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
    return segment.ipa_symbol


def each_segment(f):
    def out(word):
        syllables = []

        for syllable in word.syllables:
            onset = list(map(lambda s: f(word, s), syllable.onset))
            nucleus = list(map(lambda s: f(word, s), syllable.nucleus))
            coda = list(map(lambda s: f(word, s), syllable.coda))

            syllables.append(Syllable(onset, nucleus, coda))

        return Word(syllables)

    return out


@dataclass
class Word:
    syllables: list[Syllable]

    def show(self, printer: t.Callable[[Segment], str] = _default_word_printer) -> None:
        output = []
        for syllable in self.syllables:
            output += [*syllable.onset, *syllable.nucleus, *syllable.coda]
        print("".join([printer(x) for x in output]))
        return self

    def flatten(self):
        segments = []

        for syllable in self.syllables:
            segments += [*syllable.onset, *syllable.nucleus, *syllable.coda]

        return segments

    def surrounds(self, before, syllable, after):
        syllables = self.flatten()
        index = syllables.index(syllable)

        if (index - len(before)) < 0:
            return False

        if (index + len(after)) >= len(syllables):
            return False

        before_part = syllables[index - len(before) : index]
        after_part = syllables[index : index + len(before)]

        def matches(parts, funcs):
            return builtins.all(b(a.features) for (a, b) in zip(parts, funcs))

        if not matches(before_part, before):
            return False

        if not matches(after_part, after):
            return False

        return True

    def then(self, sound_change: t.Callable[[Word], Word]) -> t.Self:
        return sound_change(self)
