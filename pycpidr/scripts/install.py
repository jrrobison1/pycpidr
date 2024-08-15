import spacy


def download_spacy_model():
    spacy.cli.download("en_core_web_sm")


if __name__ == "__main__":
    download_spacy_model()
