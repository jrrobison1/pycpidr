from typing import List, Tuple


class WordListItem:
    def __init__(self, token: str = "", tag: str = "", is_word: bool = False, is_prop: bool = False, rule_number: int = 0):
        self.token = token
        self.tag = tag
        self.is_word = is_word
        self.is_prop = is_prop
        self.rule_number = rule_number

class WordList:
    def __init__(self, tagged_text: List[Tuple[str, str]]):
        self.items = []
        word_list_item = WordListItem("", "", False, False, 0)
        
        if not tagged_text:
            for i in range(10):
                self.items.append(word_list_item)
        
        for tagged_word in tagged_text:
            self.items.append(WordListItem(tagged_word[0], tagged_word[1], False, False, 0))