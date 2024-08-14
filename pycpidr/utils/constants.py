PUNCTUATION = frozenset({":", ",", "."})
ADJECTIVES = frozenset({"JJ", "JJR", "JJS"})
ADVERBS = frozenset({"RB", "RBR", "RBS", "WRB"})
VERBS = frozenset({"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"})
NOUNS = frozenset({"NN", "NNS", "NNP", "NNPS"})
INTERROGATIVES = frozenset({"WDT", "WP", "WPS", "WRB"})

# All the tags that, by default, are taken to be propositions
DEFAULT_PROPOSITIONS = frozenset({
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
})

# Words that are often non-propositional fillers.
FILLER = frozenset({"and", "or", "but", "if", "that", "just", "you", "know"})

# All forms of 'be'
BE = frozenset({"am", "is", "are", "was", "were", "being", "been"})

# Common negative contractions that may slip through the tagger, especially
# if accidentally typed without the apostrophe
NT = frozenset({"didn't", "didnt", "don't"
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
})

# 'Come', 'go', and their synonyms form a single proposition with following 'to' or 'from'
COME_GO = frozenset({
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
})

AUXILIARY_VERBS = frozenset({
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
})

# All forms of all verbs that take an adjective after them
LINKING_VERBS = frozenset({
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
})

# All forms of all verbs that take noun phrase + adjective after them,
# such as "make it better" or "turn it green."
CAUSATIVE_LINKING_VERBS = frozenset({
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
})

CORRELATING_CONJUNCTIONS = frozenset({"both", "either", "neither"})

# N.B. The following are not all the negative-polarity items of English,
# but only the ones that seem to form 2-word 1-concept idioms.

# Negative-polarity items where the negative, rather than this word,
# counts as the proposition; e.g., "not...yet" = "not".
NEGATIVE_POLARITY_1 = frozenset({"yet", "much", "many", "any", "anymore"})

# Negative-polarity items where this word, rather than the earlier
# negative, counts as the proposition; e.g., "not...unless" = "(n)unless".
NEGATIVE_POLARITY_2 = frozenset({"unless"})  # are there others?

SENTENCE_END = "."