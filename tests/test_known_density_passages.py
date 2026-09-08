"""
Tests for passages whose propositional idea density was calculated by hand in
peer-reviewed literature, outside of any computer program.

Unlike test_idea_density_rater.py (which tracks CPIDR 3.2's behavior), the
reference values cited in the comments here are Kintsch-school *hand* counts:
semantic propositional analyses done by trained human raters. CPIDR — and this
port of it — approximates those counts with part-of-speech heuristics, so our
numbers are expected to differ from the hand counts.

Each test therefore asserts this port's *current* output (regression
protection) while documenting the published hand count as the gold-standard
reference the output can be compared against.

The DEPID tests at the bottom run the same passages through the
dependency-based algorithm (Sirts et al., 2017) with this port's default
filter settings. DEPID tracks the hand counts noticeably better on longer
passages (dependency counting collapses much of the adjective/preposition
overcount that inflates the CPIDR numbers) but is no better on short
constructed sentences, and it has no speech mode, so fillers count toward its
word denominator.
"""

import pytest

from ideadensity.depid import depid
from ideadensity.idea_density_rater import rate_text

# Nun Study methodology sentence (Snowdon et al., 1996, JAMA 275:528-532;
# Riley et al., 2005, Neurobiology of Aging 26:341-347). Published hand
# analysis: 7 ideas / 18 words = 3.9 ideas per 10 words.
NUN_STUDY_EAU_CLAIRE = (
    "I was born in Eau Claire, Wis., on May 24, 1913 and was baptized in "
    "St. James Church."
)

# Kintsch & Keenan (1973), Cognitive Psychology 5:257-274, as reproduced in
# van Dijk & Kintsch (1983, pp. 39-40) and McKoon & Ratcliff (2008).
# Hand analysis: 4 propositions.
KINTSCH_KEENAN_ROMULUS = (
    "Romulus, the legendary founder of Rome, took the women of the Sabine "
    "by force."
)

# Kintsch & Keenan (1973). Hand analysis: 8 propositions in 16 words.
KINTSCH_KEENAN_CLEOPATRA = (
    "Cleopatra's downfall lay in her foolish trust in the fickle political "
    "figures of the Roman world."
)

# Kintsch & van Dijk (1978), Psychological Review 85:363-394, Table 1.
# Hand analysis: 46 propositions / 124 words = 0.371.
KINTSCH_VAN_DIJK_BUMPERSTICKERS = (
    "A series of violent, bloody encounters between police and Black "
    "Panther Party members punctuated the early summer days of 1969. Soon "
    "after, a group of Black students I teach at California State College, "
    "Los Angeles, who were members of the Panther Party, began to complain "
    "of continuous harassment by law enforcement officers. Among their many "
    "grievances, they complained about receiving so many traffic citations "
    "that some were in danger of losing their driving privileges. During "
    "one lengthy discussion, we realized that all of them drove automobiles "
    "with Panther Party signs glued to their bumpers. This is a report of a "
    "study that I undertook to assess the seriousness of their charges and "
    "to determine whether we were hearing the voice of paranoia or reality."
)

# Kintsch (1979), "On Comprehension" (ERIC ED173749).
# Hand analysis: 13 propositions / 36 words = 0.361.
KINTSCH_KAKRA = (
    "The Swazi tribe was at war with a neighboring tribe because of a "
    "dispute over some cattle. Among the warriors were two unmarried men, "
    "Kakra and his younger brother Gum. Kakra was killed in a battle."
)

# Turner & Greene (1977), Technical Report 63, pp. 75-76.
# Hand analysis: 22 propositions / 50 words = 0.440.
TURNER_GREENE_MERINO = (
    "Three-fourths of Australia's sheep are pure Merinos. They are popular "
    "because of the large amount of semiarid land. The Merino thrives on "
    "the grasses and low bushes which grow on semiarid plains. They are "
    "known for their heavy fleeces of fine-quality wool which bring a high "
    "price from textile manufacturers."
)

# Turner & Greene (1977), Technical Report 63, p. 78.
# Hand analysis: 27 propositions / 58 words = 0.466.
TURNER_GREENE_RECALL_PROTOCOL = (
    "The Merino is the kind of sheep commonly raised in Australia for "
    "wool. It constitutes 3/4 of the sheep there. They are popular because "
    "they thrive easily in this semiarid climate and like to eat the short "
    "bushes and grass. The Merino has a soft fleecy wool of high quality "
    "that brings good money in the world market."
)

# Chand, Baynes, Bonnici & Farias (2012), Current Protocols in Neuroscience
# 58:10.5.1-10.5.15, Example 1 / Appendix A. Hand analysis under the AID
# rubric: 50 ideas / 118 words = 4.24 ideas per 10 words.
AID_HOMETOWN_NARRATIVE = (
    "I I spent most of my uh growing up years in uh, in growing up in, in "
    "the Bronx which now has a somewhat ah se-seedy reputation. But uh, "
    "this wasn't. Well this was really middle class, um, people, school "
    "teachers, firemen, policemen, that range of uh income. Uh no one "
    "acted up there. And it was it was great. They have the. This was I "
    "think the largest housing project in the United States 2500 families. "
    "Uh and it's pretty good stores uh you know a commercial area and "
    "stuff like that. It was like a little city. Very very well "
    "maintained. We'd play in the playgrounds. And then they they "
    "sponsored um um, baseball teams and basketball teams. So I played on "
    "teams."
)


def test_nun_study_eau_claire_sentence():
    """The most-cited example sentence in the idea density literature.

    The published hand analysis lists exactly 7 ideas in 18 words (3.9 ideas
    per 10 words):
    (1) I was born, (2) born in Eau Claire, Wis., (3) born on May 24, 1913,
    (4) I was baptized, (5) was baptized in church, (6) was baptized in
    St. James Church, (7) I was born ... and was baptized.

    Our proposition count matches the hand count exactly. The word count
    differs by one (17 vs. 18) because of tokenization of the date/abbreviation
    ("Wis.", "May 24, 1913") — numerals count as words but conventions for
    splitting them differ from the Nun Study's tally.
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        NUN_STUDY_EAU_CLAIRE, speech_mode=False
    )

    assert word_count == 17
    assert proposition_count == 7
    assert idea_density == pytest.approx(0.412, abs=1e-3)


def test_kintsch_keenan_romulus_sentence():
    """Kintsch & Keenan (1973), Cognitive Psychology 5:257-274.

    The classic low-density stimulus: a ~16-word sentence hand-analyzed as
    just 4 propositions — (took, Romulus, women, by force), (founded, Romulus,
    Rome), (legendary, Romulus), (Sabine, women) — reproduced in van Dijk &
    Kintsch (1983, pp. 39-40) and McKoon & Ratcliff (2008, Psychon Bull Rev
    15:592-597). Paired with the Cleopatra sentence below: same length, twice
    the propositions, and subjects took measurably longer to read the denser
    one.

    We find 5 because POS counting can't collapse the appositive "the
    legendary founder of Rome" into the propositions a semantic analysis
    yields; prepositions like "of" and "by" each count once.
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        KINTSCH_KEENAN_ROMULUS, speech_mode=False
    )

    assert word_count == 14
    assert proposition_count == 5
    assert idea_density == pytest.approx(0.357, abs=1e-3)


def test_kintsch_keenan_cleopatra_sentence():
    """Kintsch & Keenan (1973): the high-density mate of the Romulus sentence.

    Hand-analyzed as 8 propositions in 16 words. We find 10: POS counting
    tallies every adjective and preposition ("foolish", "fickle", "political",
    "in", "of", ...) without merging them into the smaller set of semantic
    propositions the hand analysis derives. Note the direction of the error
    differs from the Romulus sentence in absolute terms but both are
    overcounts, so the hand-established density ordering (Cleopatra denser
    than Romulus) is preserved: 0.625 > 0.357.
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        KINTSCH_KEENAN_CLEOPATRA, speech_mode=False
    )

    assert word_count == 16
    assert proposition_count == 10
    assert idea_density == pytest.approx(0.625, abs=1e-3)


def test_kintsch_van_dijk_bumperstickers_paragraph():
    """Kintsch & van Dijk (1978), Psychological Review 85:363-394, Table 1.

    The opening paragraph of Heussenstam's "Bumperstickers and the cops"
    (1971), the worked example of their landmark text-comprehension model.
    Table 1 publishes the complete numbered proposition list — 1 (SERIES,
    ENCOUNTER) through 46 (OF PARANOIA, VOICE) — making this the only passage
    we know of with a fully published proposition-by-proposition hand
    analysis: 46 propositions in 124 words (0.371).

    We find 61: the usual POS overcount on adjective/preposition-heavy formal
    passages, spread over a full paragraph. (The paper's Table 2 macropropositions
    are a separate derived level and are not part of the 46.)
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        KINTSCH_VAN_DIJK_BUMPERSTICKERS, speech_mode=False
    )

    assert word_count == 124
    assert proposition_count == 61
    assert idea_density == pytest.approx(0.492, abs=1e-3)


def test_kintsch_1979_kakra_text():
    """Kintsch (1979), "On Comprehension" (ERIC ED173749).

    The Kakra/Swazi text used to illustrate cycle-by-cycle comprehension:
    hand-analyzed as 13 propositions in 36 words — 5 in the first sentence,
    6 in the second (both stated explicitly in the text), leaving 2 for the
    third by subtraction. The same text reappears in Kintsch & Vipond (1979)
    and Miller & Kintsch (1980). We find 15.
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        KINTSCH_KAKRA, speech_mode=False
    )

    assert word_count == 36
    assert proposition_count == 15
    assert idea_density == pytest.approx(0.417, abs=1e-3)


def test_turner_greene_merino_passage_text_base():
    """Turner & Greene (1977), Technical Report 63, pp. 75-76.

    The four Merino sentences already tested individually in
    test_idea_density_rater.py appear in Section 4.3 as a single recall-scoring
    template whose published text base lists exactly 22 propositions —
    1 (POSSESS, A:AUSTRALIA, O:SHEEP) through 22 (BRING, A:18, O:20, S:21) —
    in 50 words (0.440). This is the passage-level hand total for the text the
    per-sentence tests cover piecewise.

    Full scan of the report:
    https://www.colorado.edu/ics/sites/default/files/attached-files/77-63.pdf

    We find 28 propositions / 52 words; per Brown et al. (2008), CPIDR itself
    disagreed with Turner & Greene on a number of their own examples, which
    later (closed-source) CPIDR versions tried to reduce.
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        TURNER_GREENE_MERINO, speech_mode=False
    )

    assert word_count == 52
    assert proposition_count == 28
    assert idea_density == pytest.approx(0.538, abs=1e-3)


def test_turner_greene_recall_protocol():
    """Turner & Greene (1977), Technical Report 63, p. 78.

    A real subject's free recall of the Merino passage, itself fully
    propositionalized in the report: 27 numbered propositions —
    1 (ISA, MERINO, SHEEP) through 27 (POSSESS, A:1, O:26) — in 58 words
    (0.466). Interesting as natural produced language (not textbook prose),
    and because our count of 29 lands within two of the hand analysis.
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        TURNER_GREENE_RECALL_PROTOCOL, speech_mode=False
    )

    assert word_count == 58
    assert proposition_count == 29
    assert idea_density == pytest.approx(0.5, abs=1e-3)


def test_aid_rubric_hometown_narrative_speech_mode():
    """Chand, Baynes, Bonnici & Farias (2012), Current Protocols in
    Neuroscience 58:10.5.1-10.5.15 ("A Rubric for Extracting Idea Density from
    Oral Language Samples"), Example 1 / Appendix A.

    A spontaneous "Tell me about your hometown" oral narrative with a
    line-by-line published hand analysis: 50 ideas in 118 words (4.24 ideas
    per 10 words) under the AID rubric. The one spontaneous-speech passage in
    the literature with a full hand count, so it exercises speech mode
    (filler and repetition handling: "uh", "um", "I I", "it was it was").

    In speech mode our word count matches AID's hand tally of 118 exactly,
    and we find 52 propositions vs. their 50 ideas. (AID's counting rules for
    contractions and fillers differ from CPIDR's; the paper reports CPIDR 3.2
    itself tallying 121 words on their transcript, so exact agreement here is
    partly a function of transcript punctuation.)
    """
    word_count, proposition_count, idea_density, _ = rate_text(
        AID_HOMETOWN_NARRATIVE, speech_mode=True
    )

    assert word_count == 118
    assert proposition_count == 52
    assert idea_density == pytest.approx(0.441, abs=1e-3)


# ---------------------------------------------------------------------------
# DEPID (Sirts et al., 2017) on the same passages
#
# All tests use this port's default filter settings (determiner and nsubj
# filters on; the DementiaBank-tuned cc and I/you-subject filters off). On
# every written passage below, DEPID-R returns the same count as DEPID —
# duplicate dependencies only arise in spontaneous speech — so DEPID-R is
# asserted only where it differs (the AID narrative).
# ---------------------------------------------------------------------------


def test_depid_nun_study_eau_claire_sentence():
    """DEPID on the Nun Study sentence: 8 dependencies vs. the 7 hand-counted
    ideas (CPIDR port: exactly 7). Its word count of 18 matches the published
    tally exactly, though — spaCy tokenization doesn't merge "St." the way
    the CPIDR tagging path does.
    """
    density, word_count, dependencies = depid(NUN_STUDY_EAU_CLAIRE)

    assert word_count == 18
    assert len(dependencies) == 8
    assert density == pytest.approx(0.444, abs=1e-3)


def test_depid_kintsch_keenan_romulus_sentence():
    """DEPID on the Romulus sentence: 6 dependencies vs. 4 hand-counted
    propositions — worse than the CPIDR port's 5. Short constructed sentences
    are where dependency counting overshoots most in relative terms.
    """
    density, word_count, dependencies = depid(KINTSCH_KEENAN_ROMULUS)

    assert word_count == 14
    assert len(dependencies) == 6
    assert density == pytest.approx(0.429, abs=1e-3)


def test_depid_kintsch_keenan_cleopatra_sentence():
    """DEPID on the Cleopatra sentence: 10 dependencies vs. 8 hand-counted
    propositions (same count as the CPIDR port). Word count is 17 rather than
    16 because spaCy splits the possessive "Cleopatra's" into two tokens.
    The hand-established ordering (Cleopatra denser than Romulus) is
    preserved: 0.588 > 0.429.
    """
    density, word_count, dependencies = depid(KINTSCH_KEENAN_CLEOPATRA)

    assert word_count == 17
    assert len(dependencies) == 10
    assert density == pytest.approx(0.588, abs=1e-3)


def test_depid_kintsch_van_dijk_bumperstickers_paragraph():
    """DEPID on the Bumperstickers paragraph: 49 dependencies vs. the 46
    hand-counted propositions — far closer than the CPIDR port's 61, and the
    clearest case of DEPID tracking Kintsch-style hand analysis better on
    long formal passages (0.395 vs. the published 0.371).
    """
    density, word_count, dependencies = depid(KINTSCH_VAN_DIJK_BUMPERSTICKERS)

    assert word_count == 124
    assert len(dependencies) == 49
    assert density == pytest.approx(0.395, abs=1e-3)


def test_depid_kintsch_1979_kakra_text():
    """DEPID on the Kakra text: 15 dependencies vs. 13 hand-counted
    propositions — the same count as the CPIDR port.
    """
    density, word_count, dependencies = depid(KINTSCH_KAKRA)

    assert word_count == 36
    assert len(dependencies) == 15
    assert density == pytest.approx(0.417, abs=1e-3)


def test_depid_turner_greene_merino_passage_text_base():
    """DEPID on the Merino text base: 25 dependencies vs. the 22 hand-counted
    propositions — closer than the CPIDR port's 28. (Word count 53 vs. the
    port's 52: spaCy splits the hyphenated "Three-fourths".)
    """
    density, word_count, dependencies = depid(TURNER_GREENE_MERINO)

    assert word_count == 53
    assert len(dependencies) == 25
    assert density == pytest.approx(0.472, abs=1e-3)


def test_depid_turner_greene_recall_protocol():
    """DEPID on the recall protocol: 24 dependencies vs. 27 hand-counted
    propositions. Notable as the one passage here where DEPID *under*counts
    the hand analysis (the CPIDR port overcounts at 29); both land within
    three of the reference.
    """
    density, word_count, dependencies = depid(TURNER_GREENE_RECALL_PROTOCOL)

    assert word_count == 58
    assert len(dependencies) == 24
    assert density == pytest.approx(0.414, abs=1e-3)


def test_depid_aid_rubric_hometown_narrative():
    """DEPID and DEPID-R on the AID oral narrative.

    DEPID finds 54 dependencies; DEPID-R, which discards duplicate
    dependencies (exactly the noise that spontaneous-speech repetitions like
    "I I" and "it was it was" create), finds 50 — matching the published hand
    count of 50 ideas on the nose. The densities still differ from AID's
    4.24-per-10-words because DEPID has no speech mode: the "uh"/"um" fillers
    count toward its 129-word denominator, where CPIDR speech mode and the
    AID raters both count 118 words.
    """
    density, word_count, dependencies = depid(AID_HOMETOWN_NARRATIVE)

    assert word_count == 129
    assert len(dependencies) == 54
    assert density == pytest.approx(0.419, abs=1e-3)

    density_r, word_count_r, dependencies_r = depid(
        AID_HOMETOWN_NARRATIVE, is_depid_r=True
    )

    assert word_count_r == 129
    assert len(dependencies_r) == 50
    assert density_r == pytest.approx(0.388, abs=1e-3)
