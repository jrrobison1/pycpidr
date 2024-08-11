from typing import List, Tuple
from python_cpidr.idea_density_rater_rules import apply_idea_counting_rules
from python_cpidr.tagger import tag_text
from python_cpidr.word_item import WordList

def rate_text(text: str, speech_mode: bool = False) -> WordList:
    t = tag_text(text)
    
    word_list = WordList(t)
    apply_idea_counting_rules(word_list.items, speech_mode)

    wc = 0
    pc = 0
    for word in word_list.items:
        if word.is_word:
            wc += 1
        if word.is_prop:
            pc += 1

    density = pc / wc
    
    return density, word_list
