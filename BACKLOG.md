# Backlog

Polish/ideas noted while integrating ideadensity into a stylometry tool
(where it now scores rolling windows across novels):

- **Batch API**: `cpidr_many(texts)` / accepting a pre-parsed spaCy `Doc`
  would let callers tagging thousands of segments reuse one pipeline pass.
  (Workaround used downstream: score per sentence and sum counts — the
  decomposition is exact because CPIDR's rules are per-sentence.)
- **Version reporting**: `utils/version_utils.py` reads `pyproject.toml`
  from disk; `importlib.metadata.version("ideadensity")` works for
  installed copies and frozen apps alike, and drops the `tomli` runtime
  dependency on 3.11+ (`tomllib` covers 3.10 fallback if still needed).
- **Split the GUI**: `main.py` + PyQt could live as a separate package
  (or console entry point via the `gui` extra) so the library stays lean;
  the PyInstaller model-search logic in `tagger.py` is GUI-app concern.
- **Wheels/publish flow**: confirm `publish-to-pypi.yml` runs on a 3.13
  runner so the published metadata carries the widened requires-python.
- **speech_mode docs**: a README example of when to use `speech_mode=True`
  (CPIDR's original transcript heuristics) would help study authors.
- **Type hints**: `cpidr`'s tuple return could be a NamedTuple/dataclass
  (`words`, `propositions`, `density`, `word_list`) for readability in
  published-study code without breaking tuple unpacking.
