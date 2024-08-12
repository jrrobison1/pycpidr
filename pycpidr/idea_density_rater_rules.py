import logging
from typing import List
from pycpidr.word_item import WordListItem

logger = logging.getLogger(__name__)

# Tags for punctuation marks
punct = [":", ",", "."]

# Tags for adjectives
adj = ["JJ", "JJR", "JJS"]

# Tags for adverbs
adv = ["RB", "RBR", "RBS", "WRB"]

# Tags for verb forms
verb = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

# Tags for noun forms
noun = ["NN", "NNS", "NNP", "NNPS"]

# Tags for interrogatives
interrogative = ["WDT", "WP", "WPS", "WRB"]

# All the tags that, by default, are taken to be propositions
prop = [
    "CC",  # coordinating conjunction
    "CD",  # cardinal numeral
    "DT",  # determiner
    "IN",  # preposition/subordinating conj.
    "JJ",
    "JJR",
    "JJS",  # adjective
    "PDT",  # predeterminer
    "POS",  # possessive "'s" (which is not counted as a word)
    "PRP$",  # possessive pronoun
    "PP$",  # possessive pronoun
    "RB",
    "RBR",
    "RBS",  # adverbs
    "TO",  # "to" whether prep. or infinitival
    "VB",
    "VBD",
    "VBG",
    "VBN",
    "VBP",
    "VBZ",  # verbs
    "WDT",
    "WP",
    "WPS",
    "WRB",  # interrogatives/relatives
]

# Words that are often non-propositional fillers.
# A sentence consisting wholly of these is propositionless.
filler = ["and", "or", "but", "if", "that", "just", "you", "know"]

# All forms of 'be'
be = ["am", "is", "are", "was", "were", "being", "been"]

# Common negative contractions that may slip through the tagger, especially
# if accidentally typed without the apostrophe
nt = [
    "didn't",
    "didnt",
    "don't",
    "dont",
    "can't",
    "cant",
    "couldn't",
    "couldnt",
    "won't",
    "wont",
    "wouldn't",
    "wouldnt",
]

# 'Come', 'go', and their synonyms form a single proposition with following 'to' or 'from'
come_go = [
    "come",
    "comes",
    "came",
    "coming",
    "return",
    "returns",
    "returned",
    "returning",
    "arrive",
    "arrives",
    "arrived",
    "arriving",
    "go",
    "goes",
    "went",
    "gone",
    "going",
    "depart",
    "departs",
    "departed",
    "departing",
    "emanate",
    "emanates",
    "emanated",
    "emanating",
]

# All forms of all auxiliary verbs
aux = [
    "be",
    "am",
    "is",
    "are",
    "was",
    "were",
    "being",
    "been",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",  # "doing" and "done" are not aux forms
    "need",  # "needs" is not an aux
    "dare",  # "dares" is not an aux
    # and we need not include modals here
    # because the tagger does not tag them as verbs.
]

# Linking verbs:
# all forms of all verbs that take an adjective after them
link = [
    # Being
    "be",
    "am",
    "is",
    "are",
    "was",
    "were",
    "been",
    "being",
    # Becoming
    "become",
    "becomes",
    "became",
    "becoming",
    "get",
    "gets",
    "got",
    "gotten",
    "getting",
    # Seeming visually
    "look",
    "looks",
    "looked",
    "looking",
    "seem",
    "seems",
    "seemed",
    "seeming",
    "appear",
    "appears",
    "appeared",
    "appearing",
    # Seeming through other senses
    "sound",
    "sounds",
    "sounded",
    "sounding",
    "feel",
    "feels",
    "felt",
    "feeling",
    "smell",
    "smells",
    "smelled",
    "smelling",
    "taste",
    "tastes",
    "tasted",
    "tasting",
]

# Causative linking verbs:
# all forms of all verbs that take noun phrase + adjective after them,
# such as "make it better" or "turn it green."
c_link = [
    #  What else needs to be included here?
    "make",
    "makes",
    "made",
    "making",
    "turn",
    "turns",
    "turned",
    "turning",
    "paint",
    "paints",
    "painted",
    "painting",
]

# First elements of correlating conjunctions
correl = ["both", "either", "neither"]

# N.B. The following are not all the negative-polarity items of English,
# but only the ones that seem to form 2-word 1-concept idioms.

# Negative-polarity items where the negative, rather than this word,
# counts as the proposition; e.g., "not...yet" = "not".
neg_pol1 = ["yet", "much", "many", "any", "anymore"]

# Negative-polarity items where this word, rather than the earlier
# negative, counts as the proposition; e.g., "not...unless" = "(n)unless".
neg_pol2 = ["unless"]  # are there others?


# Finds the first word in the sentence containing word_list_item[i]
def beginning_of_sentence(word_list_item: WordListItem, i: int) -> int:
    j = i - 1
    while (j > 0) and (word_list_item[j].tag != ".") and (word_list_item[j].tag != ""):
        j -= 1
    return j


def match(first: str, second: str) -> bool:
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


def apply_idea_counting_rules(b: List[WordListItem], speech_mode: bool) -> None:
    #
    # This loop iterates through the WordList and may add and remove items.
    #
    # The rules look back toward the beginning from the current word; that is,
    # the rule is triggered by the last word in the pattern that it is looking for.
    # There are guaranteed to be 10 null items at the beginning of the WordList,
    # so rules do not have to worry about going past the beginning of the list.
    #
    # Most rules look at the output of prior rules; rule 200 is a good example
    # of this. The program could be speeded up by identifying rules that do *not*
    # feed a subsequent rule, and putting a "continue" statement in them, as in
    # rule 000.
    #
    # When an addition or deletion to the WordList is to be made, it must take
    # place AFTER the current location (e.g., when looking at b[i] you can add
    # or delete at i+1 but not at i-1), to prevent renumbering. Rules 003 and 004
    # contain examples of stepping backward and deleting forward.
    #
    # Remember that a deletion removes the item from the word count as well as
    # the idea count. Accordingly, items should only be deleted if they've
    # been moved or should not be counted as words.
    #
    for i in range(len(b)):
        logger.debug(f"{i} {b[i].token}/{b[i].tag}")

        # Rule group 000 - Identify words and adjust tags

        # 000
        # If it's a null item, skip the rest of these tests.
        # There will always be at least 10 null items at the beginning
        # so we can freely look back from the current position
        # without running off the beginning of the list.
        if b[i].token == "":
            continue

        # 001
        # The symbol  ^  used to mark broken-off spoken sentences
        # is an end-of-sentence marker.
        if b[i].token == "^":
            b[i].tag = "."
            b[i].rule_number = 1

        # 002
        # The item is a word if its token starts with a letter or digit
        # and its tag is not SYM (symbol).
        if b[i].token[0].isalnum() and b[i].tag != "SYM":
            b[i].is_word = True
            b[i].rule_number = 2

        # 003
        # Two cardinal numbers in immediate succession are combined into one
        # (Uncommon situation; the next one is much more common)
        if b[i].tag == "CD" and b[i - 1].tag == "CD":
            b[i - 1].token = f"{b[i - 1].token} {b[i].token}"  # adjust token
            b[i - 1].rule_number = 3
            i -= 1  # step backward 1
            del b[i + 1]  # delete forward 1

        # 004
        # Cardinal + nonalphanumeric + cardinal are combined into one token
        # (Common situation, for handling fractions, decimals, etc.)
        if (
            b[i].tag == "CD"  # current token is a number
            and len(b[i - 1].token) > 0  # preceding token contains some characters
            and not b[i - 1].token[0].isalnum()  # the first of which is nonalphanumeric
            and b[i - 2].tag == "CD"  # pre-preceding token is also a number
        ):
            b[i - 2].token = (
                b[i - 2].token + b[i - 1].token + b[i].token
            )  # adjust token
            b[i - 2].rule_number = 4
            i -= 2  # step backward 2
            del b[i + 1 : i + 3]  # delete forward 2

        # 020
        # Repetition of the form "A A" is simplified to "A".
        # The first A can be an initial substring of the second one.
        # Both remain in the word count.
        if speech_mode:
            if match(b[i - 1].token, b[i].token):
                # Mark the first A as to be ignored
                b[i - 1].is_prop = False
                b[i - 1].is_word = False
                b[i - 1].tag = ""
                b[i - 1].rule_number = 20

        # 021, 022
        # Repetition of the form "A Punct A" is simplified to "A".
        # Repetition of the form "A B A" is simplified to "A B".
        # Both A's remain in the word count.
        # The first A can be an initial substring of the second one.
        # Punct is anything with tag "." or "," or ":".
        if speech_mode:
            if match(b[i - 2].token, b[i].token) and b[i].tag not in punct:
                # Mark the first A to be ignored
                b[i - 2].tag = ""
                b[i - 2].is_word = False
                b[i - 2].is_prop = False
                b[i - 2].rule_number = 22
                # Mark the punctuation mark to be ignored
                if b[i - 1].tag in punct:  # Punct
                    b[i - 1].tag = ""
                    b[i - 1].is_word = False
                    b[i - 1].is_prop = False
                    b[i - 1].rule_number = 21

        # 023
        # Repetition of the form "A B Punct A B" is simplified to "A B".
        # Both A's and B's remain in the word count.
        # The first A (or B) can be an initial substring of the second one.
        # Punct is anything with tag "." or "," or ":".
        if speech_mode:
            if (
                match(b[i - 3].token, b[i].token)
                and match(b[i - 4].token, b[i - 1].token)
                and b[i - 2].tag in [".", ",", ":"]
            ):
                b[i - 4].tag = b[i - 3].tag = b[i - 2].tag = ""
                b[i - 4].is_word = b[i - 3].is_word = b[i - 2].is_word = False
                b[i - 4].is_prop = b[i - 3].is_prop = b[i - 2].is_prop = False
                b[i - 4].rule_number = b[i - 3].rule_number = b[i - 2].rule_number = 23

        # 050
        # 'not' and any word ending in "n't" are putatively propositions and
        # their tag is changed to NOT.
        if (
            b[i].token.lower() == "not"
            or b[i].token.lower().endswith("n't")
            or b[i].token.lower() in nt
        ):
            b[i].is_prop = True
            b[i].tag = "NOT"
            b[i].rule_number = 50

        # 054
        # 'that/DT' or 'this/DT' is a pronoun, not a determiner, if the word following it
        # is any kind of verb or adverb.
        if (b[i - 1].token.lower() == "that" or b[i - 1].token.lower() == "this") and (
            b[i] in verb or b[i] in adv
        ):
            b[i - 1].tag = "PRP"
            b[i - 1].rule_number = 54
            b[i - 1].is_prop = False

        # Rule group 100 - Word order adjustment
        # Since all the rules apply in one pass,
        # this must be approached carefully.

        # 101
        # Subject-Aux inversion
        # If the current word is an Aux,
        # and the current word is the first word of the sentence
        # or the sentence begins with an interrogative,
        # move the current word rightward to put it in front
        # of the first verb, or the end of the sentence.
        # In some cases this will move a word too far to the right,
        # but the effect on proposition counting is benign.
        if b[i].token.lower() in aux:
            bos = beginning_of_sentence(b, i)
            if bos == i or b[bos].tag in interrogative:
                # find out where to move to
                dest = i + 1
                while dest < len(b):
                    if b[dest].tag == "." or b[dest].tag in verb:
                        break
                    dest += 1

                # if movement is called for,
                if dest > i + 1:
                    # insert a copy in the new location
                    b.insert(dest, WordListItem(b[i].token, b[i].tag, True, True, 101))
                    # mark the old item as to be ignored
                    b[i].tag = ""
                    b[i].is_prop = False
                    b[i].is_word = False
                    b[i].token += "/moved"

        # Rule group 200 - Preliminary identification of propositions

        # 200
        # The tags in Prop are taken to indicate propositions.
        if b[i].tag in prop:
            b[i].is_prop = True
            b[i].rule_number = 200

        # 201
        # 'The', 'a', and 'an' are not propositions.
        if b[i].token.lower() in ["the", "an", "a"]:
            b[i].is_prop = False
            b[i].rule_number = 201

        # We get better agreement with Turner & Greene without this rule.
        # 202
        # An attributive noun (such as 'lion' in 'lion tamer') is a proposition
        # (like an adjective).
        # if self.contains(Noun, b[i].tag) and b[i - 1].tag == "NN":
        #     b[i - 1].isprop = True
        #     b[i - 1].rulenumber = 202

        # 203
        # The first word in a correlating conjunction such as
        # "either...or", "neither...nor", "both...and"
        # is not a proposition. The second word is tagged CC;
        # the first word may have been tagged CC or DT.
        if b[i].tag == "CC" and not b[i].token.lower() in correl:
            # Search back up to 10 words, but not across a sentence end.
            for j in range(i - 1, max(i - 10, -1), -1):
                if b[j].tag == ".":
                    break
                if b[j].token.lower() in correl:
                    b[j].is_prop = False
                    b[j].rule_number = 203
                    break

        # 204
        # "And then" and "or else" are each a single proposition
        if (b[i - 1].token.lower() == "and" and b[i].token.lower() == "then") or (
            b[i - 1].token.lower() == "or" and b[i].token.lower() == "else"
        ):
            b[i].is_prop = False
            b[i].rule_number = 204

        # 206
        # "To" is not a proposition when it is last word in sentence.
        if b[i].tag == "." and b[i - 1].tag == "TO":
            b[i - 1].is_prop = False
            b[i - 1].rule_number = 206

        # 207
        # Modal is a proposition when it is last word in sentence.
        if b[i].tag == "." and b[i - 1].tag == "MD":
            b[i - 1].is_prop = True
            b[i - 1].rule_number = 207

        # 210
        # Cardinal number is a proposition only if there is a noun
        # within 5 words after it (not crossing a sentence boundary).
        # This is so "in 3 parts" is 2 props but "in 1941" is only one.
        if b[i].tag == "CD":
            b[i].is_prop = False
            b[i].rule_number = 210
            # This rule looks forward up to 5 words, but not past
            # an end-of-sentence marker or the end of the WordList
            for j in range(i + 1, min(len(b), i + 6)):
                if b[j].tag == ".":
                    break
                if b[j].tag in noun:
                    b[i].is_prop = True
                    break

        # 211
        # 'Not...unless' and similar pairs count as one proposition
        # (the second word is the one counted).
        if b[i].token.lower() in neg_pol2:
            # Much the same algorithm as for correlating conjunctions.
            # Search back up to 10 words, but not across a sentence end.
            for j in range(i - 1, max(i - 10, -1), -1):
                if b[j].tag == ".":
                    break
                if b[j].tag == "NOT":
                    b[j].is_prop = False
                    b[j].rule_number = 211
                    break

        # 212
        # 'Not...any' and similar pairs count as one proposition
        # (the first word is the one counted).
        if b[i].token.lower() in neg_pol1:
            # Much the same algorithm as for correlating conjunctions.
            # Search back up to 10 words, but not across a sentence end.
            for j in range(i - 1, max(i - 10, -1), -1):
                if b[j].tag == ".":
                    break
                if b[j].tag == "NOT":
                    b[i].is_prop = False
                    b[i].rule_number = 212
                    break

        # 213
        # "Going to" is not a proposition when immediately preceding a verb.
        if (
            b[i].tag in verb
            and b[i - 1].token.lower() == "to"
            and b[i - 2].token.lower() == "going"
        ):
            b[i - 1].is_prop = False
            b[i - 1].rule_number = 213
            b[i - 2].is_prop = False
            b[i - 2].rule_number = 213

        # 214
        # "If ... then" is 1 conjunction, not two.
        # Actually checking for "if ... then (word)"
        # because "then" as last word of sentence is more likely to be adverb.
        if b[i].is_word and b[i - 1].token.lower() == "then":
            # Much the same algorithm as for correlating conjunctions.
            # Search back up to 10 words, but not across a sentence end.
            for j in range(i - 1, max(i - 10, -1), -1):
                if b[j].tag == ".":
                    break
                if b[j].token.lower() == "if":
                    b[i - 1].is_prop = False
                    b[i - 1].rule_number = 214
                    break

        # 225
        # "each other" is a pronoun (to be tagged as PRP PRP).
        if b[i].token.lower() == "other" and b[i - 1].token.lower() == "each":
            b[i].tag = b[i - 1].tag = "PRP"
            b[i].is_prop = b[i - 1].is_prop = False
            b[i].rule_number = b[i - 1].rule_number = 225

        # 230
        # "how come" and "how many" are each 1 proposition, not two.
        if (b[i].token.lower() in ["come", "many"]) and (
            b[i - 1].token.lower() == "how"
        ):
            b[i].is_prop = False
            b[i].tag = b[i - 1].tag
            b[i].rule_number = 230

        # Rule group 300 - Linking verbs

        # 301
        # Linking verb is not a proposition if followed by adj. or adv.
        # (Apparently, adverbs are frequent tagging mistakes for adjectives.)
        if (b[i].tag in adj or b[i].tag in adv) and b[i - 1].token.lower() in link:
            b[i - 1].is_prop = False
            b[i - 1].rule_number = 301

        # 302
        # "Be" is not a proposition when followed by a preposition.
        # (May want to modify this to allow an intervening adverb.)
        if b[i].tag == "IN" and b[i - 1].token.lower() in be:
            b[i - 1].is_prop = False
            b[i - 1].rule_number = 302

        # 310
        # Linking verb + Adverb + { PDT, DT } is 2 propositions
        # (e.g., "he is now the president").
        # (Would otherwise be undercounted because of rule 201).
        if b[i].tag in ["DT", "PDT"]:
            if b[i - 1].tag in adv and b[i - 2].token.lower() in link:
                b[i - 1].is_prop = True
                b[i - 1].rule_number = 310
                b[i - 2].is_prop = True
                b[i - 2].rule_number = 310

        # 311
        # Causative linking verbs: 'make it better' and similar
        # phrases do not count the adjective as a new proposition
        # (since the verb was counted).
        if b[i].tag in adj:
            # Much the same algorithm as for correlating conjunctions.
            # Search back up to 10 words, but not across a sentence boundary.
            for j in range(i - 1, max(i - 10, -1), -1):
                if b[j].tag == ".":
                    break
                if b[j].token.lower() in c_link:
                    b[i].is_prop = False
                    b[i].rule_number = 311
                    break

        # Rule group 400 - Auxiliary verbs are not propositions

        # Note that Verb is a set of tags but Aux is a set of tokens.
        # Note also that Verb includes all Aux.

        # 401
        # Aux not is one proposition, not two
        if b[i].token.lower() == "not" and b[i - 1].token.lower() in aux:
            b[i - 1].is_prop = False
            b[i - 1].rule_number = 401

        # 402
        # Aux Verb is one proposition, not two
        if b[i].tag in verb and b[i - 1].token.lower() in aux:
            b[i - 1].is_prop = False
            b[i - 1].rule_number = 402

        # 405
        # Aux NOT Verb          (NOT and the second Verb are propositions)
        # Also Aux Adverb Verb  (e.g., "had always sung", "would rather go")
        if (
            b[i].tag in verb
            and ((b[i - 1].tag == "NOT") or b[i - 1].tag in adv)
            and b[i - 2].token.lower() in aux
        ):
            b[i - 2].is_prop = False
            b[i - 2].rule_number = 405

        # Rule group 500 - Constructions involving 'to'

        # 510
        # TO VB is one proposition, not two
        if b[i].tag == "VB" and b[i - 1].tag == "TO":
            b[i - 1].is_prop = False
            b[i - 1].rule_number = 510

        # 511
        # "for ... TO VB": "for" is not a proposition
        if b[i].tag == "VB" and b[i - 1].tag == "TO":
            # Search back up to 10 words, but not across a sentence end.
            for j in range(i - 1, max(i - 10, -1), -1):
                if b[j].tag == ".":
                    break
                if b[j].token.lower() == "for":
                    b[j].is_prop = False
                    b[j].rule_number = 511
                    break

        # 512
        # "From" and "to" form a single proposition with
        # preceding "go", "come", or their synonyms.
        # (We get better agreement with Turner & Greene without this rule.)
        # if (
        #       ( (b[i].token == "to") or (b[i].token == "from") )
        #     and
        #       (Contains(ComeGo, b[i - 1].token) or Contains(ComeGo, b[i - 2].token))
        #    ):
        #   b[i].isprop = False
        #   b[i].rulenumber = 512

        # Rule group 600 - Fillers

        # 610
        # A sentence consisting entirely of probable filler words is propositionless
        if speech_mode and b[i].tag == ".":
            bos = beginning_of_sentence(b, i)
            k = 0
            for j in range(bos, i):
                if b[j].tag != "UH" and b[j].token.lower() not in filler:
                    k += 1

            if k == 0:
                for j in range(bos, i):
                    b[j].tag = ""
                    b[j].is_prop = False
                    b[j].rule_number = 610

        # 632
        # In speech mode, "like" is a filler when not immediately preceded by a form of "be".
        if speech_mode:
            if b[i].token.lower() == "like" and b[i - 1].token.lower() not in be:
                b[i].tag = ""
                b[i].is_prop = False
                b[i].rule_number = 632

        # 634
        # In speech mode, "you know" is a filler and counts as one word, not two.
        if speech_mode:
            if (
                i > 0
                and b[i - 1].token.lower() == "you"
                and b[i].token.lower() == "know"
            ):
                # back up one
                i -= 1
                # delete forward one
                del b[i + 1]
                # reset data for the current item
                b[i].token = "you_know"
                b[i].tag = ""
                b[i].is_prop = False
                b[i].is_word = True
                b[i].rule_number = 634
