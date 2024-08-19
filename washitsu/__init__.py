from __future__ import annotations

from dataclasses import dataclass
import typing as t


def and_combinator(*argv):
    return lambda x: all(arg.has(x) for arg in argv)


class Feature:
    def __and__(self, other):
        return and_combinator(self, other)

    def has(self, x: list[Feature]):
        return self in x


# Place
Bilabial = Feature()
Labiodental = Feature()
Alveolar = Feature()
PostAlveolar = Feature()
Retroflex = Feature()
Palatal = Feature()
Velar = Feature()
Uvular = Feature()
Pharyngeal = Feature()
Glottal = Feature()
# Articulation
Consonantal = Feature()
Stop = Feature()
Trill = Feature()
Tap = Feature()
Strident = Feature()
Sibilant = Feature()
Lateral = Feature()
Voiced = Feature()
Aspirated = Feature()
Sonorant = Feature()
Continuant = Feature()
Nasal = Feature()
DelayedRelease = Feature()
# Vowels
Syllabic = Feature()
High = Feature()
MidHigh = Feature()
Low = Feature()
Back = Feature()
Tense = Feature()
Rounded = Feature()

@dataclass
class Segment:
    ipa_symbol: str
    features: list[Feature]

SEGMENTS = [
    Segment("p", [Consonantal, Bilabial, Stop]),
    Segment("b", [Consonantal, Bilabial, Stop, Voiced]),
    Segment("t", [Consonantal, Alveolar, Stop]),
    Segment("d", [Consonantal, Alveolar, Stop, Voiced]),
    Segment("ʈ", [Consonantal, Retroflex, Stop]),
    Segment("ɖ", [Consonantal, Retroflex, Stop, Voiced]),
    Segment("c", [Consonantal, Palatal, Stop]),
    Segment("ɟ", [Consonantal, Palatal, Stop, Voiced]),
    Segment("k", [Consonantal, Velar, Stop]),
    Segment("g", [Consonantal, Velar, Stop, Voiced]),
    Segment("q", [Consonantal, Uvular, Stop]),
    Segment("ɢ", [Consonantal, Uvular, Stop, Voiced]),
    Segment("ʔ", [Glottal, Uvular, Stop]),
    Segment("t͡s", [Consonantal, Alveolar, Stop, DelayedRelease]),
    Segment("d͡z", [Consonantal, Alveolar, Stop, Voiced, DelayedRelease]),
    Segment("t͡ʃ", [Consonantal, PostAlveolar, Stop, DelayedRelease]),
    Segment("d͡ʒ", [Consonantal, PostAlveolar, Stop, Voiced, DelayedRelease]),
    Segment("t͡ɕ", [Consonantal, Alveolar, Palatal, Stop, DelayedRelease]),
    Segment(
        "d͡ʑ",
        [Consonantal, Alveolar, Palatal, Stop, Voiced, DelayedRelease],
    ),
    Segment("ʈ͡ʂ", [Consonantal, Retroflex, Stop, DelayedRelease]),
    Segment("ɖ͡ʐ", [Consonantal, Retroflex, Stop, Voiced, DelayedRelease]),
    Segment(
        "t͡ɬ",
        [Consonantal, Alveolar, Palatal, Stop, Lateral, DelayedRelease],
    ),
    Segment(
        "d͡ɮ",
        [Consonantal, Alveolar, Palatal, Stop, Voiced, Lateral, DelayedRelease],
    ),
    Segment("m̥", [Consonantal, Bilabial, Stop, Sonorant, Nasal]),
    Segment("ɱ̊", [Consonantal, Labiodental, Stop, Sonorant, Nasal]),
    Segment("n̥", [Consonantal, Alveolar, Stop, Sonorant, Nasal]),
    Segment("ɳ̊", [Consonantal, Retroflex, Stop, Sonorant, Nasal]),
    Segment("ɲ̊", [Consonantal, Palatal, Stop, Sonorant, Nasal]),
    Segment("ŋ̊", [Consonantal, Velar, Stop, Sonorant, Nasal]),
    Segment("ɴ̥", [Consonantal, Uvular, Stop, Sonorant, Nasal]),
    Segment("m", [Consonantal, Bilabial, Stop, Sonorant, Nasal, Voiced]),
    Segment("ɱ", [Consonantal, Labiodental, Stop, Sonorant, Nasal, Voiced]),
    Segment("n", [Consonantal, Alveolar, Stop, Sonorant, Nasal, Voiced]),
    Segment("ɳ", [Consonantal, Retroflex, Stop, Sonorant, Nasal, Voiced]),
    Segment("ɲ", [Consonantal, Palatal, Stop, Sonorant, Nasal, Voiced]),
    Segment("ŋ", [Consonantal, Velar, Stop, Sonorant, Nasal, Voiced]),
    Segment("ɴ", [Consonantal, Uvular, Stop, Sonorant, Nasal, Voiced]),
    Segment("̥ʙ", [Consonantal, Bilabial, Sonorant, Continuant, Trill]),
    Segment("̥r", [Consonantal, Alveolar, Sonorant, Continuant, Trill]),
    Segment("̥ʀ", [Consonantal, Uvular, Sonorant, Continuant, Trill]),
    Segment("̥ⱱ", [Consonantal, Labiodental, Sonorant, Continuant, Tap]),
    Segment("̥ɾ", [Consonantal, Alveolar, Sonorant, Tap]),
    Segment("̊ɽ", [Consonantal, Retroflex, Sonorant, Tap]),
    Segment("ʙ", [Consonantal, Bilabial, Sonorant, Continuant, Trill, Voiced]),
    Segment("r", [Consonantal, Alveolar, Sonorant, Continuant, Trill, Voiced]),
    Segment("ʀ", [Consonantal, Uvular, Sonorant, Continuant, Trill, Voiced]),
    Segment("ⱱ", [Consonantal, Labiodental, Sonorant, Continuant, Tap, Voiced]),
    Segment("ɾ", [Consonantal, Alveolar, Sonorant, Tap, Voiced]),
    Segment("ɽ", [Consonantal, Retroflex, Sonorant, Tap, Voiced]),
    Segment("ɸ", [Consonantal, Continuant, Bilabial, Strident]),
    Segment("β", [Consonantal, Continuant, Bilabial, Strident, Voiced]),
    Segment("f", [Consonantal, Continuant, Labiodental, Strident]),
    Segment("v", [Consonantal, Continuant, Labiodental, Strident, Voiced]),
    Segment("θ", [Consonantal, Continuant, Alveolar, Strident]),
    Segment("ð", [Consonantal, Continuant, Alveolar, Strident, Voiced]),
    Segment("s", [Consonantal, Continuant, Alveolar, Strident, Sibilant]),
    Segment("z", [Consonantal, Continuant, Alveolar, Strident, Sibilant, Voiced]),
    Segment("ɬ", [Consonantal, Continuant, Alveolar, Strident, Lateral]),
    Segment("ɮ", [Consonantal, Continuant, Alveolar, Strident, Lateral, Voiced]),
    Segment("ʃ", [Consonantal, Continuant, PostAlveolar, Strident, Sibilant]),
    Segment(
        "ʒ",
        [Consonantal, Continuant, PostAlveolar, Strident, Sibilant, Voiced],
    ),
    Segment("ʂ", [Consonantal, Continuant, Retroflex, Strident, Sibilant]),
    Segment(
        "ʐ",
        [Consonantal, Continuant, Retroflex, Strident, Sibilant, Voiced],
    ),
    Segment("ç", [Consonantal, Continuant, Palatal, Strident]),
    Segment("ʝ", [Consonantal, Continuant, Palatal, Strident, Voiced]),
    Segment(
        "ɕ",
        [Consonantal, Continuant, Alveolar, Palatal, Strident, Sibilant],
    ),
    Segment(
        "ʑ",
        [Consonantal, Continuant, Alveolar, Palatal, Strident, Sibilant, Voiced],
    ),
    Segment("x", [Consonantal, Continuant, Velar, Strident]),
    Segment("ɣ", [Consonantal, Continuant, Velar, Strident, Voiced]),
    Segment("χ", [Consonantal, Continuant, Uvular, Strident]),
    Segment("ʁ", [Consonantal, Continuant, Uvular, Strident, Voiced]),
    Segment("ħ", [Consonantal, Continuant, Pharyngeal, Strident]),
    Segment("ʕ", [Consonantal, Continuant, Pharyngeal, Strident, Voiced]),
    Segment("h", [Continuant, Glottal, Strident]),
    Segment("ɦ", [Continuant, Glottal, Strident, Voiced]),
    Segment("ʋ̥", [Consonantal, Continuant, Sonorant, Labiodental]),
    Segment("ɹ̥", [Consonantal, Continuant, Sonorant, PostAlveolar]),
    Segment("ɻ̊", [Consonantal, Continuant, Sonorant, Retroflex]),
    Segment("ɰ̊", [Continuant, Sonorant, Velar]),
    Segment("j̊", [Continuant, Sonorant, Palatal]),
    Segment("ɥ̊", [Continuant, Sonorant, Palatal, Rounded]),
    Segment("ʍ", [Continuant, Sonorant, Velar, Rounded]),
    Segment("ʋ", [Consonantal, Continuant, Sonorant, Labiodental, Voiced]),
    Segment("ɹ", [Consonantal, Continuant, Sonorant, PostAlveolar, Voiced]),
    Segment("ɻ", [Consonantal, Continuant, Sonorant, Retroflex, Voiced]),
    Segment("ɰ", [Continuant, Sonorant, Velar, Voiced]),
    Segment("j", [Continuant, Sonorant, Palatal, Voiced]),
    Segment("ɥ", [Continuant, Sonorant, Palatal, Rounded, Voiced]),
    Segment("w", [Continuant, Sonorant, Velar, Rounded, Voiced]),
    Segment("l̥", [Consonantal, Continuant, Sonorant, Alveolar, Lateral]),
    Segment("ɭ̊", [Consonantal, Continuant, Sonorant, Alveolar, Lateral]),
    Segment("ʎ̥", [Consonantal, Continuant, Sonorant, Alveolar, Lateral]),
    Segment("ʟ̥", [Consonantal, Continuant, Sonorant, Alveolar, Lateral]),
    Segment("l", [Consonantal, Continuant, Sonorant, Alveolar, Lateral, Voiced]),
    Segment("ɭ", [Consonantal, Continuant, Sonorant, Alveolar, Lateral, Voiced]),
    Segment("ʎ", [Consonantal, Continuant, Sonorant, Alveolar, Lateral, Voiced]),
    Segment("ʟ", [Consonantal, Continuant, Sonorant, Alveolar, Lateral, Voiced]),
    Segment("ɪ", [Syllabic, Voiced, Sonorant, Continuant, High]),
    Segment("ʊ", [Syllabic, Voiced, Sonorant, Continuant, High, Back, Rounded]),
    Segment("ɛ", [Syllabic, Voiced, Sonorant, Continuant, MidHigh]),
    Segment("ɔ", [Syllabic, Voiced, Sonorant, Continuant, MidHigh, Back, Rounded]),
    Segment("ɐ", [Syllabic, Voiced, Sonorant, Continuant, Low]),
    Segment("i", [Syllabic, Voiced, Sonorant, Continuant, High, Tense]),
    Segment("u", [Syllabic, Voiced, Sonorant, Continuant, High, Back, Rounded, Tense]),
    Segment("e", [Syllabic, Voiced, Sonorant, Continuant, MidHigh, Tense]),
    Segment(
        "o", [Syllabic, Voiced, Sonorant, Continuant, MidHigh, Back, Rounded, Tense]
    ),
    Segment("a", [Syllabic, Voiced, Sonorant, Continuant, Low, Tense]),
    Segment("ə", [Syllabic, Voiced, Sonorant, Continuant]),
]

@dataclass
class Syllable:
    onset: list[Segment]
    nucleus: list[Segment]
    coda: list[Segment]
    supersegmentals: list[Feature]


@dataclass
class Word:
    syllables: list[Syllable]

    def then(self, sound_change: t.Callable[[Segment], Segment]) -> t.Self:
        pass
