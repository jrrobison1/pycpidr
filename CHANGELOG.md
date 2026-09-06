# Changelog

## 0.6.0

- **Python 3.13/3.14 support.** The `<3.13` upper bound is now
  `<3.15`, tracking spaCy's supported range — the code was already
  compatible (full test suite passes on 3.13); only packaging blocked
  installation.
- **Dependency fixes for 3.13:**
  - Replaced the deprecated `python-levenshtein` wrapper (whose pinned
    version fails to build on 3.13) with modern `levenshtein>=0.25`,
    which ships 3.13 wheels. The `from Levenshtein import ratio` import
    is unchanged.
  - Removed an unused `import pkg_resources` in `tagger.py`, which made
    the library require `setuptools<81` on Python 3.13 (newer setuptools
    no longer ships `pkg_resources`).
- **PyQt6 is now an optional extra.** Library users (`pip install
  ideadensity`) no longer pull in the GUI toolkit; the desktop app needs
  `pip install ideadensity[gui]`.
- **CPIDR tagging is ~3x faster.** The spaCy pipeline now disables the
  parser, NER, lemmatizer, and attribute ruler — CPIDR only reads
  Penn Treebank tags (`token.tag_`), so results are identical. (DEPID
  still loads the full pipeline; it needs the dependency parse.)
- CI now tests Python 3.10–3.13.
- `tomli` is now only required on Python 3.10 (3.11+ uses the standard
  library's `tomllib`).
