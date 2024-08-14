from typing import Callable, List, Optional

from pycpidr.word_item import WordListItem
from pycpidr.utils.constants import SENTENCE_END

MAX_LOOKBACK = 10


def is_beginning_of_sentence(word_list_item: WordListItem, i: int) -> int:
    """
    Finds the index of the beginning of the sentence containing the word at index i.

    Args:
        word_list_item (WordListItem): The list of word items to search through.
        i (int): The index of the current word.

    Returns:
        int: The index of the beginning of the sentence, or 0 if not found.
    """
    j = i - 1
    while (j > 0) and (word_list_item[j].tag != SENTENCE_END) and (word_list_item[j].tag != ""):
        j -= 1
    return j


def is_repetition(first: str, second: str) -> bool:
    """
    Determines whether a word is likely to be a repetition of another.
    The first word may be incomplete, e.g. "hesi- hesitation".
    """
    if not first or not second:
        return False
    if first == second:
        return True
    if first.endswith("-"):
        first = first[:-1]  # final hyphen drop
    if len(second) > 3 and first not in ("a", "an") and second.startswith(first):
        return True
    return False


def search_backwards(word_list: List[WordListItem], i: int, condition: Callable[[WordListItem], bool]) -> Optional[WordListItem]:
    """
    Search backwards in the word list for an item that satisfies the given condition.

    Args:
        word_list (List[WordListItem]): The list of word items to search through.
        i (int): The starting index for the backward search.
        condition (Callable[[WordListItem], bool]): A function that takes a WordListItem and returns a boolean.

    Returns:
        Optional[WordListItem]: The first WordListItem that satisfies the condition, or None if not found.

    Note:
        The search stops if it encounters a sentence end or reaches the beginning of the list.
        The search is limited to MAX_LOOKBACK items.
    """
    for j in range(i - 1, max(i - MAX_LOOKBACK, -1), -1):
        prev_word = word_list[j]
        if prev_word.tag == SENTENCE_END:
            break
        if condition(prev_word):
            return word_list[j]
    return None