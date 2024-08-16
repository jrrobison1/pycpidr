import pytest
from pycpidr.utils.word_search_utils import beginning_of_sentence, is_repetition
from pycpidr.word_item import WordListItem
from pycpidr.utils.constants import SENTENCE_END


def create_word_list(tokens, tags):
    return [WordListItem(token=t, tag=tag) for t, tag in zip(tokens, tags)]


def test_beginning_of_sentence_middle():
    words = create_word_list(
        ["This", "is", "a", "sentence", ".", "Another", "one", "."],
        [
            "PLC_TAG",
            "PLC_TAG",
            "PLC_TAG",
            "PLC_TAG",
            SENTENCE_END,
            "PLC_TAG",
            "PLC_TAG",
            SENTENCE_END,
        ],
    )
    assert beginning_of_sentence(words, 6) == 5


def test_beginning_of_sentence_start():
    words = create_word_list(
        ["This", "is", "a", "sentence", "."],
        ["PLC_TAG", "PLC_TAG", "PLC_TAG", "PLC_TAG", SENTENCE_END],
    )
    assert beginning_of_sentence(words, 2) == 0


def test_beginning_of_sentence_end():
    words = create_word_list(
        ["This", "is", "a", "sentence", "."],
        ["PLC_TAG", "PLC_TAG", "PLC_TAG", "PLC_TAG", SENTENCE_END],
    )
    assert beginning_of_sentence(words, 4) == 0


def test_beginning_of_sentence_single_word():
    words = create_word_list(["Word"], [""])
    assert beginning_of_sentence(words, 0) == 0


def test_beginning_of_sentence_multiple_sentences():
    words = create_word_list(
        ["First", ".", "Second", ".", "Third", "sentence", "."],
        [
            "PLC_TAG",
            SENTENCE_END,
            "PLC_TAG",
            SENTENCE_END,
            "PLC_TAG",
            "PLC_TAG",
            SENTENCE_END,
        ],
    )
    assert beginning_of_sentence(words, 5) == 4


def test_is_repetition():
    # Test exact match
    assert is_repetition("word", "word") == True

    # Test incomplete word with hyphen
    assert is_repetition("hesi-", "hesitation") == True

    # Test non-repetition
    assert is_repetition("cat", "dog") == False

    # Test empty strings
    assert is_repetition("", "") == False
    assert is_repetition("word", "") == False
    assert is_repetition("", "word") == False

    # Test short words (3 characters or less)
    assert is_repetition("a", "apple") == False
    assert is_repetition("an", "another") == False
    assert is_repetition("the", "theocracy") == False

    # Test words that start the same but aren't repetitions
    assert is_repetition("car", "carpet") == False
