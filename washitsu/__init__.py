from __future__ import annotations

from dataclasses import dataclass
import typing as t
import random

import builtins

def all(*argv):
    return lambda x: builtins.all(arg.has(x) for arg in argv)

def any(*argv):
    return lambda x: builtins.any(arg.has(x) for arg in argv)

@dataclass
class Feature:
    name: str

    def __call__(self, *args, **kwargs):
        return self.has(*args, **kwargs)

    def __and__(self, other):
        return all(self, other)

    def __or__(self, other):
        return any(self, other)

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
    Segment("u", [syllabic, voiced, sonorant, continuant, high, back, labialized, tense]),
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


@dataclass
class Word:
    syllables: list[Syllable]

    def then(self, sound_change: t.Callable[[Segment], Segment]) -> t.Self:
        pass
