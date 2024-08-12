import spacy

_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def tag_text(text, nlp=get_nlp()):
    _nlp = nlp

    doc = _nlp(text)
    tagged_tokens = [(token.text, token.tag_) for token in doc]

    return tagged_tokens
