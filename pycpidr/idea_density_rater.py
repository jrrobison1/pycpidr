from typing import Tuple
from pycpidr.idea_density_rater_rules import apply_idea_counting_rules
from pycpidr.tagger import tag_text
from pycpidr.word_item import WordList


def rate_text(text: str, speech_mode: bool = False) -> Tuple[int, int, float, WordList]:
    """
    Rate the idea density of the given text.

    Args:
        text (str): The input text to analyze.
        speech_mode (bool): Whether to use speech mode for idea counting rules.

    Returns:
        Tuple[int, int, float, WordList]: A tuple containing:
            - word_count: Total number of words.
            - proposition_count: Number of propositions.
            - density: Idea density (propositions / words).
            - word_list: Processed WordList object.
    """
    if text is None:
        return 0, 0, 0.0, WordList([])

    tagged_text = tag_text(text)
    word_list = WordList(tagged_text)
    apply_idea_counting_rules(word_list.items, speech_mode)

    word_count, proposition_count = count_words_and_propositions(word_list)
    density = proposition_count / word_count if word_count > 0 else 0.0

    return word_count, proposition_count, density, word_list


def count_words_and_propositions(word_list: WordList) -> Tuple[int, int]:
    """
    Count the number of words and propositions in the given WordList.

    Args:
        word_list (WordList): The processed WordList object.

    Returns:
        Tuple[int, int]: A tuple containing the word count and proposition count.
    """
    word_count = sum(1 for word in word_list.items if word.is_word)
    proposition_count = sum(1 for word in word_list.items if word.is_proposition)

    return word_count, proposition_count
