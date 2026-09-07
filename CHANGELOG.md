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
- Executable build workflows install the `gui` extra (required now that
  PyQt6 is optional), drop the obsolete `tomli` hidden imports (stdlib
  `tomllib` is used on the 3.13 build Python), and build on Python 3.13.
- **Citation guidance overhauled.** New CITATION.cff (GitHub's cite
  button now works); the README's Citing section explains what to cite:
  the tool always, Brown et al. (2008) when using cpidr, Sirts et al.
  (2017) when using depid. The Sirts reference is corrected from "arXiv
  preprint" to its published CoNLL 2017 venue, and both papers carry DOIs.
- New `ideadensity.reproducibility_info()`: returns the ideadensity,
  spaCy, and spaCy-model versions for reporting in a study's methods
  section — scores depend on the tagger/parser, so these matter.
