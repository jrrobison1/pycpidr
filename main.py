import sys
from python_cpidr.idea_density_rater import rate_text


def main(text):
    _, _, density, word_list = rate_text(text, speech_mode=False)

    print(f"Density: {density}")
    print(f"Word list:")
    for word in word_list.items:
        print(
            f"Token: [{word.token}], tag: [{word.tag}], is_word: [{word.is_word}], is_prop: [{word.is_prop}], rule_number: [{word.rule_number}]"
        )


if __name__ == "__main__":
    main(sys.argv[1])
