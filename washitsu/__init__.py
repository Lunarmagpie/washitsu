from __future__ import annotations
import itertools
import copy
from dataclasses import dataclass
import random
import typing as t
from pprint import pprint


def lists_are_equal(a, b):
    return all(x in b for x in a) and all(x in a for x in b)


def subset_amount(a, b):
    amount = 0
    for item in a:
        if item in b:
            amount += 1
    return len(a) - amount


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
high = Feature("high")
mid_high = Feature("Midhigh")
low = Feature("Low")
back = Feature("back")
tense = Feature("Tense")
# Diacritic
labialized = Feature("Labialized")
palatalized = Feature("Palatalized")
velarized = Feature("Velarized")
pharyngealized = Feature("Pharyngealized")


@dataclass
class Segment:
    ipa_symbol: str
    features: list[Feature]

    def __add__(self, other: Feature):
        changed = copy.copy(self)
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

DIACRITICS = [
    Segment("ʰ", [aspirated]),
    Segment("ʷ", [labialized]),
    Segment("ʲ", [palatalized]),
    Segment("ˠ", [velarized]),
    Segment("ˤ", [pharyngealized]),
    Segment("̃", [nasal]),
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
    subset_amounts = []
    for big_seg in SEGMENTS:
        subset_amounts += [(big_seg, subset_amount(segment.features, big_seg.features))]

    subset_amounts: list[tuple[Segment, int]] = sorted(subset_amounts, key=lambda x: x[1])

    chosen_seg = subset_amounts[0][0]
    old_features = copy.copy(segment).features
    for feature in chosen_seg.features:
        if feature in old_features:
            old_features.remove(feature)

    print(old_features)

    return subset_amounts[0][0].ipa_symbol

    raise Exception(f"Can not find matching segment: {segment.features}")


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
