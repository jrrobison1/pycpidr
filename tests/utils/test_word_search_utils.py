import pytest
from pycpidr.utils.word_search_utils import beginning_of_sentence
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
