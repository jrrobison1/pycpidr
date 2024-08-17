from typing import Callable, List, Optional, Tuple
import spacy

proposition_dependencies = frozenset(["advcl", "advmod", "amod", "appos", "cc", "csubj", "csubjpass", "det", "neg", "npadvmod", "nsubj", "nsubjpass", "nummod", "poss", "predet", "preconj", "prep", "quantmod", "tmod", "vmod"])
excluded_determiners = frozenset(["a", "an", "the"])
excluded_nsubj = frozenset(["it", "this"])

def is_i_you_subject(sent: spacy.tokens.Span) -> bool:
    for token in sent:
        if token.text.lower() in ["i", "you"] and token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
            return False
    return True

def is_excluded_determiner(token: spacy.tokens.Token) -> bool:
    if token.dep_ == "det" and token.text.lower() in excluded_determiners:
        return False
    return True

def is_excluded_nsubj(token: spacy.tokens.Token) -> bool:
    if token.dep_ == "nsubj" and token.text.lower() in excluded_nsubj:
        return False
    return True

def depid(text: str, sentence_filters: Optional[List[Callable[[spacy.tokens.Span], bool]]] = None, token_filters: Optional[List[Callable[[spacy.tokens.Token], bool]]] = None) -> Tuple[float, int, List[Tuple[str, str, str]]]:
    """
    Calculate the idea density of a given text using dependency parsing.

    Args:
        text (str): The input text to analyze.
        sentence_filters (Optional[List[Callable[[spacy.tokens.Span], bool]]]): A list of functions to filter sentences.
        token_filters (Optional[List[Callable[[spacy.tokens.Token], bool]]]): A list of functions to filter tokens.

    Returns:
        Tuple[float, int, List[Tuple[str, str, str]]]: A tuple containing:
            - density (float): The calculated idea density.
            - word_count (int): The number of words in the text.
            - dependencies (List[Tuple[str, str, str]]): A list of dependencies, each represented as (token, dependency, head).
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word_count = len([token for token in doc if not token.is_punct and not token.is_space])

    if sentence_filters:
        filtered_sents = [sent for sent in doc.sents if all(filter_func(sent) for filter_func in sentence_filters)]
        doc = spacy.tokens.Doc(doc.vocab, words=[token.text for sent in filtered_sents for token in sent])
        doc = nlp(doc)  
    
    dependencies = []
    
    for token in doc:
        if not token.dep_ in proposition_dependencies:
            continue
        if token_filters and any(not filter_func(token) for filter_func in token_filters):
            continue
        dependencies.append((token.text, token.dep_, token.head.text))

    if word_count > 0:
        density = len(dependencies) / word_count
    else:
        density = 0.0

    return density, word_count, dependencies
    
text = "what else can I tell you about the picture? The picture is black, and the tree is bright green."
deps = depid(text, sentence_filters=[is_i_you_subject], token_filters=[is_excluded_determiner, is_excluded_nsubj])

density, word_count, dependencies = depid(text, sentence_filters=[is_i_you_subject], token_filters=[is_excluded_determiner, is_excluded_nsubj])
print(f"Density: {density}")
print(f"Word count: {word_count}")
print(f"Dependencies: {dependencies}")
