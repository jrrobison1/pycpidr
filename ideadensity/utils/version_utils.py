import importlib.metadata
from pathlib import Path
import spacy

try:  # Python 3.11+
    import tomllib as tomli
except ModuleNotFoundError:
    import tomli


def get_version():
    """
    Get the ideadensity package version.
    
    Tries to get the version from:
    1. pyproject.toml file (preferred for development)
    2. Package metadata (when installed and no pyproject.toml)
    3. Hardcoded fallback if both methods fail
    
    Returns:
        str: The version string
    """
    # First, try to find the version in pyproject.toml (preferred)
    try:
        current_dir = Path(__file__).resolve().parent
        # Search up to 4 levels up from current file to find pyproject.toml
        for _ in range(5):  # current dir + 4 levels up
            pyproject_path = current_dir / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    pyproject_data = tomli.load(f)
                version = pyproject_data.get("tool", {}).get("poetry", {}).get("version")
                if version:
                    return version
            current_dir = current_dir.parent
    except Exception:
        pass
        
    # If pyproject.toml not found, try package metadata
    try:
        return importlib.metadata.version("ideadensity")
    except importlib.metadata.PackageNotFoundError:
        pass
    
    # Fallback to hardcoded version
    return "0.4.1"

def get_spacy_version_info():
    """Get the spaCy version and model information.
    
    Returns:
        tuple: (spacy_version, model_name, model_version)
    """
    spacy_version = spacy.__version__
    try:
        nlp = spacy.load("en_core_web_sm")
        model_name = "en_core_web_sm"
        model_version = nlp.meta["version"]
    except:
        model_name = "en_core_web_sm"
        model_version = "not loaded"
    
    return spacy_version, model_name, model_version


def reproducibility_info() -> dict:
    """Version information to report alongside published results.

    Idea-density scores depend on the tagger/parser, so reproducing a
    study's numbers requires the ideadensity version, the spaCy version,
    and the spaCy model version. Paste this into your methods section:

        >>> import ideadensity
        >>> ideadensity.reproducibility_info()
        {'ideadensity': '0.6.0', 'spacy': '3.8.11',
         'spacy_model': 'en_core_web_sm', 'spacy_model_version': '3.8.0'}

    Returns:
        dict: ideadensity, spacy, spacy_model, and spacy_model_version.
    """
    spacy_version, model_name, model_version = get_spacy_version_info()
    return {
        "ideadensity": get_version(),
        "spacy": spacy_version,
        "spacy_model": model_name,
        "spacy_model_version": model_version,
    }