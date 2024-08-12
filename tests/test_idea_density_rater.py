import pytest

import spacy
from python_cpidr.idea_density_rater import rate_text


nlp = spacy.load("en_core_web_sm")


def test_turner_greene_sentence_1():
    sentence = "Louise and Ann went to the movies last night."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 9
    assert proposition_count == 4
    assert idea_density == pytest.approx(0.444, abs=1e-3)


def test_turner_greene_sentence_2():
    sentence = "They met Charlie there."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 4
    assert proposition_count == 2
    assert idea_density == pytest.approx(0.5, abs=1e-3)


def test_turner_greene_sentence_3():
    sentence = "Afterwards they all went for a chocolate sundae, but the ice cream parlor was closed."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 15
    assert proposition_count == 6
    assert idea_density == pytest.approx(0.4, abs=1e-3)


def test_turner_greene_sentence_4():
    sentence = "Three fourths of Australia's sheep are pure Merinos."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 8
    assert proposition_count == 4
    assert idea_density == pytest.approx(0.5, abs=1e-3)


def test_turner_greene_sentence_5():
    sentence = "They are popular because of the large amount of semiarid land."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 11
    assert proposition_count == 6
    assert idea_density == pytest.approx(0.545, abs=1e-3)


def test_turner_greene_sentence_6():
    sentence = "The Merino thrives on the grasses and low bushes which grow on semiarid plains."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 14
    assert proposition_count == 8
    assert idea_density == pytest.approx(0.571, abs=1e-3)


@pytest.mark.skip(
    reason="This test fails because spacy is marking 'heavy' as JJ instead of NN."
)
def test_turner_greene_sentence_7():
    sentence = "They are known for their heavy fleeces of fine-quality wool which bring a high price from textile manufacturers."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 18
    assert proposition_count == 9
    assert idea_density == pytest.approx(0.5, abs=1e-3)


@pytest.mark.skip(
    reason="This test fails because spacy is marking 'out' as RP instead of IN."
)
def test_turner_greene_sentence_8():
    sentence = "...I unbolted the door and went out."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 7
    assert proposition_count == 4
    assert idea_density == pytest.approx(0.571, abs=1e-3)


def test_turner_greene_sentence_9():
    sentence = "It was cool outside in the early morning, and the sun had not yet dried the dew that had come when the wind died down."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 25
    assert proposition_count == 11
    assert idea_density == pytest.approx(0.44, abs=1e-3)


def test_turner_greene_sentence_10():
    sentence = "I hunted around in the shed behind the inn and found a sort of mattock, and went down toward the stream to try and dig some worms for bait."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 29
    assert proposition_count == 16
    assert idea_density == pytest.approx(0.552, abs=1e-3)


def test_turner_greene_sentence_11():
    sentence = "The stream was clear and shallow but it did not look trouty."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 12
    assert proposition_count == 6
    assert idea_density == pytest.approx(0.5, abs=1e-3)


@pytest.mark.skip(
    reason="This test fails because spacy is marking 'grassy' as NNP instead of JJ."
)
def test_turner_greene_sentence_12():
    sentence = "On the grassy bank where it was damp, I drove the mattock into the earth and loosened a chunk of sod."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 21
    assert proposition_count == 9
    assert idea_density == pytest.approx(0.429, abs=1e-3)


def test_turner_greene_sentence_13():
    sentence = "There were worms underneath."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 4
    assert proposition_count == 2
    assert idea_density == pytest.approx(0.5, abs=1e-3)


def test_turner_greene_sentence_14():
    sentence = "They slid out of sight as I lifted the sod and I dug carefully and got a good many."

    word_count, proposition_count, idea_density, word_list = rate_text(sentence, nlp)

    assert word_count == 19
    assert proposition_count == 12
    assert idea_density == pytest.approx(0.632, abs=1e-3)
