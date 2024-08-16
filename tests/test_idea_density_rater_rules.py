import pytest
from pycpidr.idea_density_rater_rules import identify_words_and_adjust_tags
from pycpidr.word_item import WordListItem
from pycpidr.utils.constants import SENTENCE_END, RuleNumber

NUMBER_OF_BLANK_WORD_ITEMS = 10
FIRST_WORD_INDEX = NUMBER_OF_BLANK_WORD_ITEMS


@pytest.fixture
def create_word_list():
    def _create_word_list(tokens_and_tags):
        return [WordListItem() for _ in range(NUMBER_OF_BLANK_WORD_ITEMS)] + [
            WordListItem(token, tag) for token, tag in tokens_and_tags
        ]

    return _create_word_list


def test_sentence_end_marker(create_word_list):
    word_list = create_word_list([("^", "")])
    identify_words_and_adjust_tags(word_list, FIRST_WORD_INDEX, False)
    assert word_list[FIRST_WORD_INDEX].tag == SENTENCE_END
    assert word_list[FIRST_WORD_INDEX].rule_number == RuleNumber.SENTENCE_END_MARKER


def test_alphanumeric_word(create_word_list):
    word_list = create_word_list([("hello", "NN")])
    identify_words_and_adjust_tags(word_list, FIRST_WORD_INDEX, False)
    assert word_list[FIRST_WORD_INDEX].is_word == True
    assert word_list[FIRST_WORD_INDEX].rule_number == RuleNumber.ALPHANUMERIC_WORD


def test_combine_consecutive_cardinals(create_word_list):
    word_list = create_word_list([("10", "CD"), ("20", "CD"), ("thirty", "CD")])
    identify_words_and_adjust_tags(word_list, FIRST_WORD_INDEX + 1, False)
    assert len(word_list) == NUMBER_OF_BLANK_WORD_ITEMS + 2
    assert word_list[FIRST_WORD_INDEX].token == "10 20"
    assert (
        word_list[FIRST_WORD_INDEX].rule_number
        == RuleNumber.COMBINE_CONSECUTIVE_CARDINALS
    )


def test_combine_cardinals_with_separator(create_word_list):
    word_list = create_word_list([("10", "CD"), (".", ""), ("5", "CD")])
    identify_words_and_adjust_tags(word_list, FIRST_WORD_INDEX + 2, False)
    assert len(word_list) == NUMBER_OF_BLANK_WORD_ITEMS + 1
    assert word_list[FIRST_WORD_INDEX].token == "10.5"
    assert (
        word_list[FIRST_WORD_INDEX].rule_number
        == RuleNumber.COMBINE_CARDINALS_WITH_SEPARATOR
    )


def test_repetition_in_speech_mode(create_word_list):
    word_list = create_word_list([("the", "DT"), ("the", "DT")])
    identify_words_and_adjust_tags(word_list, FIRST_WORD_INDEX + 1, True)
    assert word_list[FIRST_WORD_INDEX].is_proposition == False
    assert word_list[FIRST_WORD_INDEX].is_word == False
    assert word_list[FIRST_WORD_INDEX].tag == ""
    assert word_list[FIRST_WORD_INDEX].rule_number == 20


def test_negation_identification(create_word_list):
    word_list = create_word_list([("not", "")])
    identify_words_and_adjust_tags(word_list, FIRST_WORD_INDEX, False)
    assert word_list[FIRST_WORD_INDEX].is_proposition == True
    assert word_list[FIRST_WORD_INDEX].tag == "NOT"
    assert word_list[FIRST_WORD_INDEX].rule_number == 50


def test_determiner_to_pronoun_adjustment(create_word_list):
    word_list = create_word_list([("that", "DT"), ("runs", "VBZ")])

    identify_words_and_adjust_tags(word_list, FIRST_WORD_INDEX + 1, False)

    assert word_list[FIRST_WORD_INDEX].tag == "PRP"
    assert word_list[FIRST_WORD_INDEX].is_proposition == False
    assert word_list[FIRST_WORD_INDEX].rule_number == 54
