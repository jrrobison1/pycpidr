from typing import Callable, List, Optional, Set, Tuple

import spacy

PROPOSITION_DEPENDENCIES = frozenset(
    [
        "advcl",
        "advmod",
        "amod",
        "appos",
        "cc",
        "csubj",
        "csubjpass",
        "det",
        "neg",
        "npadvmod",
        "nsubj",
        "nsubjpass",
        "nummod",
        "poss",
        "predet",
        "preconj",
        "prep",
        "quantmod",
        "tmod",
        "vmod",
    ]
)
EXCLUDED_DETERMINERS = frozenset(["a", "an", "the"])
EXCLUDED_NSUBJ = frozenset(["it", "this"])

_nlp = None


def get_nlp():
    """
    Load and return the spaCy English language model.

    Returns:
        spacy.lang.en.English: The loaded spaCy English language model.
    """
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError(
                "The 'en_core_web_sm' model is not installed. Please install it using: `python -m spacy download en_core_web_sm`."
            )
    return _nlp


def is_i_you_subject(sent: spacy.tokens.Span) -> bool:
    """
    Check if the sentence contains 'I' or 'you' as the subject of the main verb.

    This function is a sentence filter used by (Sirts et al., 2017) in their DEPID algorithm.
    It returns False if the sentence contains 'I' or 'you' as the subject of the root verb,
    and True otherwise.

    Args:
        sent (spacy.tokens.Span): A spaCy sentence span to analyze.

    Returns:
        bool: False if 'I' or 'you' is the subject of the main verb, True otherwise.
    """
    for token in sent:
        if (
            token.text.lower() in ["i", "you"]
            and token.dep_ == "nsubj"
            and token.head.dep_ == "ROOT"
        ):
            return False
    return True


def is_excluded_determiner(token: spacy.tokens.Token) -> bool:
    """
    Check if a token is an excluded determiner.

    This function is a token filter used by (Sirts et al., 2017) in their DEPID algorithm.
    It returns False if the token is a determiner ('det') and is in the list of excluded determiners,
    and True otherwise.

    Args:
        token (spacy.tokens.Token): A spaCy token to analyze.

    Returns:
        bool: False if the token is an excluded determiner, True otherwise.
    """
    if token.dep_ == "det" and token.text.lower() in EXCLUDED_DETERMINERS:
        return False
    return True


def is_excluded_cc(token: spacy.tokens.Token) -> bool:
    """
    Check if a token is an excluded coordinating conjunction.

    (Sirts et al., 2017) exclude cc dependencies from the proposition list in their DEPID algorithm.
    It returns False if the token is a coordinating conjunction ('cc'),
    and True otherwise.

    Args:
        token (spacy.tokens.Token): A spaCy token to analyze.

    Returns:
        bool: False if the token is a coordinating conjunction, True otherwise.
    """
    if token.dep_ == "cc":
        return False
    return True


def is_excluded_nsubj(token: spacy.tokens.Token) -> bool:
    """
    Check if a token is an excluded nominal subject.

    This function is a token filter used by (Sirts et al., 2017 in their DEPID algorithm.
    It returns False if the token is a nominal subject ('nsubj') and is in the list of excluded subjects,
    and True otherwise.

    Args:
        token (spacy.tokens.Token): A spaCy token to analyze.

    Returns:
        bool: False if the token is an excluded nominal subject, True otherwise.
    """
    if token.dep_ == "nsubj" and token.text.lower() in EXCLUDED_NSUBJ:
        return False
    return True


SENTENCE_FILTERS = [is_i_you_subject]
TOKEN_FILTERS = [is_excluded_determiner, is_excluded_nsubj, is_excluded_cc]


def depid(
    text: str,
    is_depid_r: bool = False,
    sentence_filters: Optional[
        List[Callable[[spacy.tokens.Span], bool]]
    ] = SENTENCE_FILTERS,
    token_filters: Optional[List[Callable[[spacy.tokens.Token], bool]]] = TOKEN_FILTERS,
) -> (
    Tuple[float, int, List[Tuple[str, str, str]]]
    | Tuple[float, int, Set[Tuple[str, str, str]]]
):
    """
    Calculate the idea density of a given text using the DEPID algorithm.

    This function implements the DEPID (Dependency-based Propositional Idea Density) algorithm
    as described by (Sirts et al., 2017). It processes the input text, applies optional sentence
    and token filters, and calculates the idea density based on the remaining dependencies.

    Args:
        text (str): The input text to analyze.
        is_depid_r (bool, optional):
            Counts _distinct_ dependencies. If True, returns dependencies as a set instead
            of a list. Defaults to False.
        sentence_filters (Optional[List[Callable[[spacy.tokens.Span], bool]]], optional):
            A list of functions to filter sentences. Defaults to SENTENCE_FILTERS.
        token_filters (Optional[List[Callable[[spacy.tokens.Token], bool]]], optional):
            A list of functions to filter tokens. Defaults to TOKEN_FILTERS.

    Returns:
        Tuple[float, int, List[Tuple[str, str, str]]] | Tuple[float, int, Set[Tuple[str, str, str]]]:
            A tuple containing:
            - The calculated idea density (float)
            - The word count (int)
            - The list or set of dependencies, each as a tuple (token, dependency, head)

    Note:
        The function uses spaCy for text processing and applies the specified filters
        to refine the analysis according to the DEPID algorithm.
    """

    nlp = get_nlp()
    doc = nlp(text)

    word_count = len(
        [token for token in doc if not token.is_punct and not token.is_space]
    )

    if sentence_filters:
        filtered_sents = [
            sent
            for sent in doc.sents
            if all(filter_func(sent) for filter_func in sentence_filters)
        ]
        doc = spacy.tokens.Doc(
            doc.vocab, words=[token.text for sent in filtered_sents for token in sent]
        )
        doc = nlp(doc)

    if is_depid_r:
        dependencies = set()
    else:
        dependencies = []

    for token in doc:
        if not token.dep_ in PROPOSITION_DEPENDENCIES:
            continue
        if token_filters and any(
            not filter_func(token) for filter_func in token_filters
        ):
            continue
        if is_depid_r:
            dependencies.add((token.text, token.dep_, token.head.text))
        else:
            dependencies.append((token.text, token.dep_, token.head.text))

    if word_count > 0:
        density = len(dependencies) / word_count
    else:
        density = 0.0

    return density, word_count, dependencies
