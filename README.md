# pycpidr

Python library port of the Computerized Propositional Idea Density Rater (CPIDR) 3.2.

pycpidr is a Python library that determines the propositional idea density of an English text automatically. This project is a port of the original CPIDR 3.2 software, which was written in C#, to Python for use as a library. The goal is to make this functionality more accessible to Python developers and researchers.

## What is Idea Density?

Idea density, also known as propositional density, is a measure of the amount of information conveyed relative to the number of words used. It's calculated by dividing the number of expressed propositions by the number of words. This metric has applications in various fields, including linguistics, cognitive science, and healthcare research.

## Installation

### Using pip
1. Install the package
```bash
pip install pycpidr
```

2. Download the required spaCy model:
```bash
python -m spacy download en_core_web_sm
```

### Using poetry

```bash
poetry add pycpidr
python -m spacy download en_core_web_sm
```

## Usage

Here's a simple example of how to use PyCPIDR:

```python
from pycpidr import rate_text

text = "The quick brown fox jumps over the lazy dog."
word_count, proposition_count, density, word_list = rate_text(text)

print(f"Word count: {word_count}")
print(f"Proposition count: {proposition_count}")
print(f"Idea density: {density:.3f}")

# Analyzing speech
speech_text = "Um, you know, I think that, like, the weather is nice today."
word_count, proposition_count, density, word_list = rate_text(speech_text, speech_mode=True)

print(f"Speech mode - Idea density: {density:.3f}")

# Detailed word analysis
for word in word_list.items:
    if word.is_word:
        print(f"Token: {word.token}, Tag: {word.tag}, Is proposition: {word.is_proposition}")
```

## Speech Mode

PyCPIDR supports a speech mode that handles common speech patterns and fillers differently from written text. When analyzing transcripts or spoken language, use the `speech_mode=True` parameter for more accurate results.

## Requirements

- Python 3.10+
- spaCy 3.7.5+

## Development Setup

To set up the development environment:

1. Clone the repository
2. Install Poetry if you haven't already: `pip install poetry`
3. Install project dependencies: `poetry install`
4. Install the required spaCy model: `poetry run python -m spacy download en_core_web_sm`
5. Activate the virtual environment: `poetry shell`

## Running Tests

To run the tests, use pytest:

```bash
pytest tests/
```

## Parity with CPIDR 3.2
Because this port uses spaCy as a part-of-speech tagger instead of the original program's MontyLingua, there is a very slight difference in the reported idea density. This port includes unit tests containing 847 words of text.
This project: 434 propositions. 0.512 idea density
CPIDR 3.2: 436 propositions. 0.515 idea density

For more information about the original CPIDR 3.2, please visit [CASPR's official page](http://ai1.ai.uga.edu/caspr/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure that your code passes all tests and follows the project's coding style.

## License
This project is licensed under the GNU General Public License v2.0. See the [LICENSE](LICENSE) file for details.

As this is a port of the original CPIDR 3.2, which was released under GPL v2, this project maintains the same license to comply with the terms of the original software.