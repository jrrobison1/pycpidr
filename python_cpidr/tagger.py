import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download("punkt_tab")
nltk.download('averaged_perceptron_tagger_eng')

def tag_text(text):
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    
    return tagged_tokens


